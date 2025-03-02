import base64
import gzip
import json
import os
import urllib.parse
from io import StringIO

import pandas as pd
import streamlit as st

import lactate_thresholds as lt
import lactate_thresholds.zones as zones


def get_base_url():
    import urllib.parse

    session = st.runtime.get_instance()._session_mgr.list_active_sessions()[0]
    st_base_url = urllib.parse.urlunparse(
        [session.client.request.protocol, session.client.request.host, "", "", "", ""]
    )
    return st_base_url


def data_placeholder() -> pd.DataFrame:
    df = pd.DataFrame.from_dict(
        [
            {
                "step": 1,
                "length": 8,
                "intensity": 100,
                "rel_power": 1.3,
                "heart_rate": 113,
                "lactate_4": 1.0,
                "lactate_8": 1.0,
                "cadence": 102,
                "rpe": 6,
            },
            {
                "step": 2,
                "length": 8,
                "intensity": 140,
                "rel_power": 1.8,
                "heart_rate": 126,
                "lactate_4": 1.0,
                "lactate_8": 1.0,
                "cadence": 100,
                "rpe": 7,
            },
            {
                "step": 3,
                "length": 8,
                "intensity": 180,
                "rel_power": 2.3,
                "heart_rate": 137,
                "lactate_4": 0.9,
                "lactate_8": 0.9,
                "cadence": 100,
                "rpe": 10,
            },
            {
                "step": 4,
                "length": 8,
                "intensity": 220,
                "rel_power": 2.8,
                "heart_rate": 151,
                "lactate_4": 1.0,
                "lactate_8": 1.0,
                "cadence": 98,
                "rpe": 12,
            },
            {
                "step": 5,
                "length": 8,
                "intensity": 260,
                "rel_power": 3.3,
                "heart_rate": 168,
                "lactate_4": 1.9,
                "lactate_8": 1.9,
                "cadence": 98,
                "rpe": 16,
            },
            {
                "step": 6,
                "length": 8,
                "intensity": 300,
                "rel_power": 3.8,
                "heart_rate": 181,
                "lactate_4": 3.3,
                "lactate_8": 3.8,
                "cadence": 94,
                "rpe": 18,
            },
            {
                "step": 7,
                "length": 8,
                "intensity": 340,
                "rel_power": 4.3,
                "heart_rate": 190,
                "lactate_4": 6.4,
                "lactate_8": 7.5,
                "cadence": 92,
                "rpe": 19,
            },
        ]
    )
    return lt.clean_data(df, lactate_col="lactate_8")


def main():
    st.set_page_config(
        page_title="Lactate Thresholds",
        page_icon="🌟",
        layout="wide",
        initial_sidebar_state="auto",
    )

    def snapshot_url():
        snapshot = {
            "measurements": df_editor.to_json(index=False, orient="records"),
            "lt1": st.session_state.lt_df.loc[0, "intensity"],
            "lt2": st.session_state.lt_df.loc[1, "intensity"],
            "zone_type": st.session_state.zone_type,
            "comments": st.session_state.test_comments,
        }

        json_snapshot = json.dumps(snapshot)
        # Compress JSON data using gzip and add version indicator
        compressed_data = gzip.compress(json_snapshot.encode("utf-8"))
        # Prefix with 'gz:' to indicate compressed format
        base64_str = "gz:" + base64.b64encode(compressed_data).decode("utf-8")
        # URL encode the snapshot parameter to handle special characters
        encoded_snapshot = urllib.parse.quote(base64_str)
        st.session_state.snapshot_url = f"{get_base_url()}/?snapshot={encoded_snapshot}"

    @st.cache_data
    def init_measurements_df() -> pd.DataFrame:
        """Initialize measurements dataframe with placeholder data."""
        return data_placeholder()
    
    def load_from_snapshot(snapshot_b64: str) -> tuple[pd.DataFrame, dict] | tuple[None, None]:
        """
        Load measurements from a snapshot.
        
        Returns:
            A tuple containing:
            - DataFrame with measurements data
            - Dictionary with snapshot parameters (lt1, lt2, zone_type, comments)
        """
        try:
            # URL decode the snapshot parameter
            encoded_data = urllib.parse.unquote(snapshot_b64)
            if encoded_data.startswith("gz:"):
                # New format: decompress gzipped data
                compressed_data = base64.b64decode(encoded_data[3:])  # Skip 'gz:' prefix
                json_data = gzip.decompress(compressed_data).decode("utf-8")
                snapshot = json.loads(json_data)
            else:
                # Legacy format: direct base64 decode
                snapshot = json.loads(base64.b64decode(encoded_data).decode("utf-8"))
            
            df = pd.read_json(StringIO(snapshot["measurements"]))
            
            # Return all parameters instead of setting them directly
            params = {
                "lt1_setting": snapshot["lt1"],
                "lt2_setting": snapshot["lt2"],
                "zone_type": snapshot["zone_type"],
                "test_comments": snapshot.get("comments", "")
            }
            
            return df, params
        except Exception as e:
            st.warning(f"Error loading snapshot: {e}")
            return None, None


    
    # Use a session state flag to track if we've already loaded the snapshot
    if "initialized" not in st.session_state:
        st.session_state.initialized = False

    if not st.session_state.initialized:
        # Check if a snapshot exists and load it, otherwise use placeholder data
        snapshot_param = st.query_params.get("snapshot")
        if snapshot_param:
            df, params = load_from_snapshot(snapshot_param)
            if df is None:  # If there was an error loading the snapshot
                df = init_measurements_df()
            else:
                # Set session state variables from the returned parameters
                # only if they don't already exist
                for key, value in params.items():
                    if key not in st.session_state:
                        st.session_state[key] = value
                
                # Mark that we've loaded the snapshot
                st.session_state.snapshot_loaded = True
        else:
            df = init_measurements_df()
            if "test_comments" not in st.session_state:
                st.session_state.test_comments = ""
            if "zone_type" not in st.session_state:
                st.session_state.zone_type = "Seiler 3-zone"  # Default zone type

    # Ensure intensity and length are float types
    df['intensity'] = df['intensity'].astype(float)
    df['length'] = df['length'].astype(float)
    st.title("Lactate Thresholds")
    
    st.text_area(
        "Comments",
        key="test_comments",
        placeholder="Add any comments about this test...",
        label_visibility="collapsed",
    )

    df_editor = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "intensity": st.column_config.NumberColumn("intensity", step=0.1),
            "length": st.column_config.NumberColumn("length", step=0.1, format="%.2f"),
        },
    )
    results = lt.determine(df_editor)

    def construct_lt_df():
        lt_df = pd.DataFrame([results.lt1_estimate.model_dump(), results.lt2_estimate.model_dump()])
        lt_df.insert(0, "Threshold", ["LT1", "LT2"])
        st.session_state.lt_df = lt_df

    def construct_zones_df():
        if st.session_state.zone_type == "Seiler 3-zone":
            zones_df = zones.seiler_3_zones(results)

        elif st.session_state.zone_type == "Seiler 5-zone":
            zones_df = zones.seiler_5_zones(results)

        elif st.session_state.zone_type == "Friel 7-zone":
            zones_df = zones.friel_7_zones_running(results)

        else:
            zones_df = pd.DataFrame()

        st.session_state.zones_df = zones_df

    def update_lt():
        results.calc_lt1_lt2_estimates(lt1=st.session_state.lt1_setting, lt2=st.session_state.lt2_setting)
        construct_lt_df()
        construct_zones_df()

    hcol1, hcol2 = st.columns([0.7, 0.3])
    with hcol1:
        st.checkbox("Show fit line", key="fit_line", value=True)
        st.altair_chart(
            lt.plot.lactate_intensity_plot(results, show_fit_line=st.session_state.fit_line),
            use_container_width=True,
        )

        st.altair_chart(
            lt.plot.heart_rate_intensity_plot(results, show_fit_line=st.session_state.fit_line),
            use_container_width=True,
        )

    if "lt_df" not in st.session_state:
        construct_lt_df()

    with hcol2:
        st.markdown("**Set LT1 and LT2 intensity values**")
        st.markdown(":gray[Defaults to estimated values]")

        if "lt1_setting" not in st.session_state:
            st.session_state.lt1_setting = st.session_state.lt_df.loc[0, "intensity"]

        if "lt2_setting" not in st.session_state:
            st.session_state.lt2_setting = st.session_state.lt_df.loc[1, "intensity"]

        col1, col2 = st.columns(2)
        with col1:
            st.number_input(
                "LT1",
                on_change=update_lt,
                key="lt1_setting",
            )
        with col2:
            st.number_input(
                "LT2",
                on_change=update_lt,
                key="lt2_setting",
            )

        st.dataframe(st.session_state.lt_df, hide_index=True, use_container_width=True)

        st.selectbox(
            "Select zones type",
            ["Seiler 3-zone", "Seiler 5-zone", "Friel 7-zone"],
            key="zone_type",
            on_change=construct_zones_df,
        )

        if "zones_df" not in st.session_state:
            construct_zones_df()

        st.dataframe(st.session_state.zones_df, hide_index=True, use_container_width=True)

        with st.popover("Link to snapshot"):
            snapshot_url()
            st.code(st.session_state.snapshot_url)


def start():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    import subprocess
    import sys

    subprocess.run(["streamlit", "run", f"{current_dir}/app.py"] + sys.argv[1:])


if __name__ == "__main__":
    main()
