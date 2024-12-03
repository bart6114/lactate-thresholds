import logging

import pandas as pd

from lactate_thresholds import process


def test_interpolation(test_instances):
    df = pd.DataFrame.from_dict(test_instances["simple"])
    dfc = process.lactate_data(df)
    dfi = process.interpolate(dfc, include_baseline=False)
    logging.info(process.determine_ltp(dfc, dfi))


def test_interpolation_watt_intensity(test_instances):
    df = pd.DataFrame.from_dict(test_instances["cycling1"])
    dfc = process.lactate_data(df, lactate_col="lactate_8")
    dfi = process.interpolate(dfc, include_baseline=False)
    logging.info(process.determine_ltp(dfc, dfi))
