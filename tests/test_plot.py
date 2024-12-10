import logging

import pandas as pd

from lactate_thresholds import determine
from lactate_thresholds.plot import heart_rate_intensity_plot, lactate_intensity_plot


def test_lactate_intensity_plot(test_instances, test_output_dir):
    df = pd.DataFrame.from_dict(test_instances["simple"])
    df2 = determine(df)
    logging.info(df2)
    chart = lactate_intensity_plot(df2)
    chart.save(f"{test_output_dir}/lactate_intensity_plot.html")


def test_lactate_intensity_plot2(test_instances, test_output_dir):
    df = pd.DataFrame.from_dict(test_instances["cycling2"])
    df2 = determine(df, lactate_col="lactate_8")
    chart = lactate_intensity_plot(df2)
    chart.save(f"{test_output_dir}/lactate_intensity_plot2.html")


def test_heartrate_intensity_plot(test_instances, test_output_dir):
    df = pd.DataFrame.from_dict(test_instances["simple"])
    df2 = determine(df)
    logging.info(df2)
    chart = heart_rate_intensity_plot(df2)
    chart.save(f"{test_output_dir}/heartrate_intensity_plot.html")
