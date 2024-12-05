import matplotlib.pyplot as plt
import seaborn as sns

from lactate_thresholds.types import LactateThresholdResults


def lactate_intensity_plot(x: LactateThresholdResults):
    plt.figure(figsize=(10, 8))

    sns.scatterplot(
        x="intensity",
        y="lactate",
        data=x.clean_data[x.clean_data["intensity"] > 0],
        color="black",
    )

    sns.lineplot(
        x="intensity",
        y="lactate",
        data=x.clean_data[x.clean_data["intensity"] > 0],
        color="black",
        alpha=0.4,
    )

    sns.lineplot(x="intensity", y="lactate", data=x.interpolated_data)

    shapes = {
        "ltp1": ("o", "red"),
        "ltp2": ("s", "blue"),
        "mod_dmax": ("D", "green"),
        "loglog": ("X", "orange"),
    }

    for key, (shape, color) in shapes.items():
        r = getattr(x, key)
        if r is not None:
            plt.scatter(
                r.intensity,
                r.lactate,
                color=color,
                marker=shape,
                label=key,
                s=100,  # size of the marker
            )

    plt.legend(title="Thresholds")
    plt.xlabel("Intensity")
    plt.ylabel("Lactate")
    plt.title("Lactate Intensity Plot")



import altair as alt
import pandas as pd

def lactate_intensity_plot_altair(x: LactateThresholdResults):
    # Base chart for scatter and line plot of clean_data
    clean_data = x.clean_data[x.clean_data["intensity"] > 0]
    base = alt.Chart(clean_data).encode(
        x=alt.X("intensity:Q", title="Intensity", scale=alt.Scale(domain=[clean_data["intensity"].min() - 1, clean_data["intensity"].max() + 1])),
        y=alt.Y("lactate:Q", title="Lactate")
    ).properties(
        width=800,
        height=600
    )
    
    scatter = base.mark_point(color="black", opacity=0.1).properties(title="Lactate Intensity Plot")
    line = base.mark_line(color="black", opacity=0.1)
    
    # Line plot for interpolated_data
    interpolated_data = alt.Chart(x.interpolated_data).mark_line().encode(
        x="intensity:Q",
        y="lactate:Q"
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
            threshold_data.append({
                "intensity": r.intensity,
                "lactate": r.lactate,
                "threshold": key,
                "shape": shape,
                "color": color
            })
    
    threshold_df = pd.DataFrame(threshold_data)
    
    thresholds = alt.Chart(threshold_df).mark_point(size=100).encode(
        x="intensity:Q",
        y="lactate:Q",
        shape=alt.Shape("threshold:N", scale=alt.Scale(
            domain=list(shapes.keys()),
            range=[shapes[key][0] for key in shapes.keys()]
        )),
        color=alt.Color("threshold:N", scale=alt.Scale(
            domain=list(shapes.keys()),
            range=[shapes[key][1] for key in shapes.keys()]
        )),
        tooltip=["threshold", "intensity", "lactate"]
    )
    
    
    # Combine all layers
    chart = (scatter + line + interpolated_data + thresholds).interactive()

    
    return chart
