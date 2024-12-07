import os

import pandas as pd
import streamlit as st

import lactate_thresholds as lt


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
                "feeling": "Zeer zeer licht",
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
                "feeling": "Zeer zeer licht",
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
                "feeling": "Zeer licht",
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
                "feeling": "Tamelijk licht",
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
                "feeling": "Zwaar",
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
                "feeling": "Zwaar",
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
                "feeling": "Zeer zeer zwaar",
            },
        ]
    )
    return lt.clean_data(df, lactate_col="lactate_8")


def main():
    st.title("Lactate Thresholds")

    df = data_placeholder()
    edited_df = st.data_editor(df, num_rows="dynamic")

    ld = lt.determine(edited_df)
    lt.lactate_intensity_plot(ld)
    st.altair_chart(lt.plot.lactate_intensity_plot(ld), use_container_width=True)


def start():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.system(f"streamlit run {current_dir}/app.py")


if __name__ == "__main__":
    main()
