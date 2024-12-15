import altair as alt
import pandas as pd

from lactate_thresholds.types import LactateThresholdResults


def lactate_intensity_plot(x: LactateThresholdResults, show_fit_line: bool = True):
    clean_data = x.clean_data[x.clean_data["intensity"] > 0]
    interpolated_data = x.interpolated_data

    base = (
        alt.Chart(clean_data)
        .encode(
            x=alt.X(
                "intensity:Q",
                title="Intensity",
                scale=alt.Scale(
                    domain=[
                        clean_data["intensity"].min() - 1,
                        clean_data["intensity"].max() + 1,
                    ]
                ),
            ),
            y=alt.Y("lactate:Q", title="Lactate"),
        )
        .properties(width=800, height=600)
    )

    points_orig = base.mark_point(color="grey", opacity=0.3).properties(title="Lactate Intensity Plot")
    line_orig = base.mark_line(color="grey", opacity=0.3)

    if show_fit_line:
        line_interpolated = alt.Chart(interpolated_data).mark_line().encode(x="intensity:Q", y="lactate:Q")

    # Add thresholds with shapes and colors
    threshold_data = []
    shapes = {
        "ltp1": ("circle", "#FF6347"),  # tomato
        "ltp2": ("square", "#4682B4"),  # steelblue
        "mod_dmax": ("diamond", "#32CD32"),  # limegreen
        "loglog": ("cross", "#FFA500"),  # orange
        "obla_2": ("triangle-up", "#8A2BE2"),  # blueviolet
        "obla_4": ("triangle-down", "#8A2BE2"),  # blueviolet
        "lt1_estimate": (
            "M0,.5L.6,.8L.5,.1L1,-.3L.3,-.4L0,-1L-.3,-.4L-1,-.3L-.5,.1L-.6,.8L0,.5Z",
            "#FFD700",
        ),  # gold
        "lt2_estimate": (
            "M0,.5L.6,.8L.5,.1L1,-.3L.3,-.4L0,-1L-.3,-.4L-1,-.3L-.5,.1L-.6,.8L0,.5Z",
            "#FFD700",
        ),  # gold
    }

    for key, (shape, color) in shapes.items():
        r = getattr(x, key)
        if r is not None:
            threshold_data.append(
                {
                    "intensity": r.intensity,
                    "lactate": r.lactate,
                    "threshold": key,
                    "shape": shape,
                    "color": color,
                }
            )

    threshold_df = pd.DataFrame(threshold_data)

    thresholds = (
        alt.Chart(threshold_df)
        .mark_point(size=150, filled=True, strokeOpacity=1, fillOpacity=1)
        .encode(
            x="intensity:Q",
            y="lactate:Q",
            shape=alt.Shape(
                "threshold:N",
                scale=alt.Scale(
                    domain=list(shapes.keys()),
                    range=[shapes[key][0] for key in shapes.keys()],
                ),
            ),
            color=alt.Color(
                "threshold:N",
                scale=alt.Scale(
                    domain=list(shapes.keys()),
                    range=[shapes[key][1] for key in shapes.keys()],
                ),
            ),
        )
    )

    # Add interactive selection tied to interpolated data
    nearest = alt.selection_point(nearest=True, on="mouseover", fields=["intensity"], empty=False)

    selectors = (
        alt.Chart(interpolated_data).mark_point().encode(x="intensity:Q", opacity=alt.value(0)).add_params(nearest)
    )

    points = (
        alt.Chart(interpolated_data)
        .mark_point(size=50, color="red")
        .encode(
            x="intensity:Q",
            y="lactate:Q",
            opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
        )
    )

    rules = (
        alt.Chart(interpolated_data)
        .mark_rule(color="gray")
        .encode(x="intensity:Q")
        .transform_filter(nearest)
        .properties(
            height=600  # Ensure the rule spans the full height of the graph
        )
    )

    vertical_dotted_line = (
        alt.Chart(pd.DataFrame({"lactate": [x.baseline.lactate]}))
        .mark_rule(strokeDash=[5, 5], color="purple")
        .encode(y=alt.Y("lactate:Q"))
        .properties(width=800, height=600)
    )

    layers = [
        points_orig,
        line_orig,
        vertical_dotted_line,
        thresholds,
        selectors,
        points,
        rules,
    ]

    if show_fit_line:
        layers.append(line_interpolated)

    chart = (
        alt.layer(*layers)
        .interactive()
        .encode(
            tooltip=[
                alt.Tooltip("intensity:Q", format=".1f"),
                alt.Tooltip("lactate:Q", format=".1f"),
                alt.Tooltip("heart_rate:Q", format=".0f"),
            ]
        )
    )

    return chart


def heart_rate_intensity_plot(x: LactateThresholdResults, show_fit_line: bool = True):
    clean_data = x.clean_data[x.clean_data["intensity"] > 0]
    interpolated_data = x.interpolated_data

    base = (
        alt.Chart(clean_data)
        .encode(
            x=alt.X(
                "intensity:Q",
                title="Intensity",
                scale=alt.Scale(
                    domain=[
                        clean_data["intensity"].min() - 1,
                        clean_data["intensity"].max() + 1,
                    ]
                ),
            ),
            y=alt.Y(
                "heart_rate:Q",
                title="Heart Rate (bpm)",
                scale=alt.Scale(
                    domain=[
                        clean_data["heart_rate"].min() - 10,
                        clean_data["heart_rate"].max() + 10,
                    ]
                ),
            ),
        )
        .properties(width=800, height=600)
    )

    points_orig = base.mark_point(color="grey", opacity=0.3).properties(title="Heart Rate Intensity Plot")
    line_orig = base.mark_line(color="grey", opacity=0.3)

    if show_fit_line:
        line_interpolated = alt.Chart(interpolated_data).mark_line().encode(x="intensity:Q", y="heart_rate:Q")

    # Add thresholds with shapes and colors
    threshold_data = []
    shapes = {
        "ltp1": ("circle", "#FF6347"),  # tomato
        "ltp2": ("square", "#4682B4"),  # steelblue
        "mod_dmax": ("diamond", "#32CD32"),  # limegreen
        "loglog": ("cross", "#FFA500"),  # orange
        "obla_2": ("triangle-up", "#8A2BE2"),  # blueviolet
        "obla_4": ("triangle-down", "#8A2BE2"),  # blueviolet
        "lt1_estimate": (
            "M0,.5L.6,.8L.5,.1L1,-.3L.3,-.4L0,-1L-.3,-.4L-1,-.3L-.5,.1L-.6,.8L0,.5Z",
            "#FFD700",
        ),  # gold
        "lt2_estimate": (
            "M0,.5L.6,.8L.5,.1L1,-.3L.3,-.4L0,-1L-.3,-.4L-1,-.3L-.5,.1L-.6,.8L0,.5Z",
            "#FFD700",
        ),  # gold
    }

    for key, (shape, color) in shapes.items():
        r = getattr(x, key)
        if r is not None:
            threshold_data.append(
                {
                    "intensity": r.intensity,
                    "heart_rate": r.heart_rate,
                    "threshold": key,
                    "shape": shape,
                    "color": color,
                }
            )

    threshold_df = pd.DataFrame(threshold_data)

    thresholds = (
        alt.Chart(threshold_df)
        .mark_point(size=150, filled=True, strokeOpacity=1, fillOpacity=1)
        .encode(
            x="intensity:Q",
            y="heart_rate:Q",
            shape=alt.Shape(
                "threshold:N",
                scale=alt.Scale(
                    domain=list(shapes.keys()),
                    range=[shapes[key][0] for key in shapes.keys()],
                ),
            ),
            color=alt.Color(
                "threshold:N",
                scale=alt.Scale(
                    domain=list(shapes.keys()),
                    range=[shapes[key][1] for key in shapes.keys()],
                ),
            ),
        )
    )

    # Add interactive selection tied to interpolated data
    nearest = alt.selection_point(nearest=True, on="mouseover", fields=["intensity"], empty=False)

    selectors = (
        alt.Chart(interpolated_data).mark_point().encode(x="intensity:Q", opacity=alt.value(0)).add_params(nearest)
    )

    points = (
        alt.Chart(interpolated_data)
        .mark_point(size=50, color="red")
        .encode(
            x="intensity:Q",
            y="heart_rate:Q",
            opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
        )
    )

    rules = (
        alt.Chart(interpolated_data)
        .mark_rule(color="gray")
        .encode(x="intensity:Q")
        .transform_filter(nearest)
        .properties(
            height=600  # Ensure the rule spans the full height of the graph
        )
    )

    layers = [
        points_orig,
        line_orig,
        thresholds,
        selectors,
        points,
        rules,
    ]

    if show_fit_line:
        layers.append(line_interpolated)

    chart = (
        alt.layer(*layers)
        .interactive()
        .encode(
            tooltip=[
                alt.Tooltip("intensity:Q", format=".1f"),
                alt.Tooltip("heart_rate:Q", format=".0f"),
            ]
        )
    )

    return chart
