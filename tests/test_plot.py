import matplotlib.pyplot as plt
import pandas as pd

from lactate_thresholds import determine
from lactate_thresholds.plot import lactate_intensity_plot


def test_lactate_intensity_plot(test_instances, test_output_dir):
    df = pd.DataFrame.from_dict(test_instances["simple"])
    df2 = determine(df)
    lactate_intensity_plot(df2)
    plt.savefig(f"{test_output_dir}/lactate_intensity_plot.png")
    plt.close()


def test_lactate_intensity_plot2(test_instances, test_output_dir):
    df = pd.DataFrame.from_dict(test_instances["cycling2"])
    df2 = determine(df, lactate_col="lactate_8")
    lactate_intensity_plot(df2)
    plt.savefig(f"{test_output_dir}/lactate_intensity_plot2.png")
    plt.close()
