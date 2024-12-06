import altair as alt
import pandas as pd

from lactate_thresholds.types import LactateThresholdResults


def lactate_intensity_plot(x: LactateThresholdResults):
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

    scatter = base.mark_point(color="black", opacity=0.1).properties(
        title="Lactate Intensity Plot"
    )
    line_measurement = base.mark_line(color="black", opacity=0.1)

    interpolated_line = (
        alt.Chart(interpolated_data).mark_line().encode(x="intensity:Q", y="lactate:Q")
    )

    # Add thresholds with shapes and colors
    threshold_data = []
    shapes = {
        "ltp1": ("circle", "#FF6347"),  # tomato
        "ltp2": ("square", "#4682B4"),  # steelblue
        "mod_dmax": ("diamond", "#32CD32"),  # limegreen
        "loglog": ("cross", "#FFA500"),  # orange
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
        .mark_point(size=100)
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
            tooltip=["threshold", "intensity", "lactate"],
        )
    )

    # Add interactive selection tied to interpolated data
    nearest = alt.selection_point(nearest=True, on="mouseover", fields=["intensity"], empty=False)

    selectors = (
        alt.Chart(interpolated_data)
        .mark_point()
        .encode(x="intensity:Q", opacity=alt.value(0))
        .add_params(nearest)
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

    text = (
        alt.Chart(interpolated_data)
        .mark_text(align="left", dx=5, dy=-5)
        .encode(
            x="intensity:Q",
            y="lactate:Q",
            text=alt.condition(
                nearest, alt.Text("lactate:Q", format=".2f"), alt.value("")
            ),
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

    # Combine all layers
    chart = alt.layer(
        scatter,
        line_measurement,
        interpolated_line,
        vertical_dotted_line,
        thresholds,
        selectors,
        points,
        text,
        rules,
    ).interactive()

    return chart
