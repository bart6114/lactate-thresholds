import matplotlib.pyplot as plt
import seaborn as sns

from lactate_thresholds.types import LactateThresholdResults


def lactate_intensity_plot(x: LactateThresholdResults):
    plt.figure(figsize=(10, 8))
    sns.lineplot(x="intensity", y="lactate", data=x.interpolated_data)
    ## add the LTPs
    plt.axvline(x.ltp1.intensity, color="green", linestyle="--")
    plt.axvline(x.ltp2.intensity, color="red", linestyle="--")
    ## add info next to the LTP lines about hearrate, lactate and intensity

    intensity_range = (
        x.interpolated_data["intensity"].max() - x.interpolated_data["intensity"].min()
    )
    offset = intensity_range * 0.01  # Adjust this multiplier as needed

    plt.text(
        x.ltp1.intensity + offset,  # Dynamic offset for LT1
        x.interpolated_data["lactate"].max(),
        f"LT1\nint: {round(x.ltp1.intensity, 2)}\nlactate: {round(x.ltp1.lactate, 1)}\nhr: {int(x.ltp1.heart_rate)}",
        verticalalignment="top",
    )

    plt.text(
        x.ltp2.intensity + offset,  # Dynamic offset for LT2
        x.interpolated_data["lactate"].max(),
        f"LT2\nint: {round(x.ltp2.intensity, 2)}\nlactate: {round(x.ltp2.lactate, 1)}\nhr: {int(x.ltp2.heart_rate)}",
        verticalalignment="top",
    )

    # plot the original measurements as black dots
    sns.scatterplot(
        x="intensity",
        y="lactate",
        data=x.clean_data[x.clean_data["intensity"] > 0],
        color="black",
    )
