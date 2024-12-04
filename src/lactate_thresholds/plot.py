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
            "mod_dmax": ("D", "green")
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
                s=100  # size of the marker
            )

    plt.legend(title="Thresholds")
    plt.xlabel("Intensity")
    plt.ylabel("Lactate")
    plt.title("Lactate Intensity Plot")