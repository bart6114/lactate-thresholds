import logging

import pandas as pd

from lactate_thresholds import determine, methods, process


def test_interpolation(test_instances):
    df = pd.DataFrame.from_dict(test_instances["simple"])
    dfc = process.clean_data(df)
    dfi = methods.interpolate(dfc, include_baseline=False)
    logging.info(methods.determine_ltp(dfc, dfi))


def test_interpolation_watt_intensity(test_instances):
    df = pd.DataFrame.from_dict(test_instances["cycling1"])
    dfc = process.clean_data(df, lactate_col="lactate_8")
    dfi = methods.interpolate(dfc, include_baseline=False)
    logging.info(methods.determine_ltp(dfc, dfi))

    # do the same for cycling2
    df = pd.DataFrame.from_dict(test_instances["cycling2"])
    dfc = process.clean_data(df, lactate_col="lactate_8")
    dfi = methods.interpolate(dfc, include_baseline=False)
    logging.info(methods.determine_ltp(dfc, dfi))


def test_convenience_determine(test_instances):
    df = pd.DataFrame.from_dict(test_instances["cycling2"])
    determine(df, lactate_col="lactate_4")


def test_moddmax(test_instances):
    df = pd.DataFrame.from_dict(test_instances["cycling2"])
    dfc = process.clean_data(df, lactate_col="lactate_8")
    dfi = methods.interpolate(dfc, include_baseline=False)
    logging.info(methods.determine_mod_dmax(dfc, dfi))


def test_loglog(test_instances):
    df = pd.DataFrame.from_dict(test_instances["cycling2"])
    dfc = process.clean_data(df, lactate_col="lactate_8")
    di = methods.interpolate(dfc, include_baseline=False)
    logging.info(methods.determine_loglog(dfc, di))


def test_baseline_plus(test_instances):
    df = pd.DataFrame.from_dict(test_instances["cycling2"])
    dfc = process.clean_data(df, lactate_col="lactate_8")
    di = methods.interpolate(dfc, include_baseline=False)
    logging.info(methods.determine_baseline(dfc, di, 0.5))


def test_obla(test_instances):
    df = pd.DataFrame.from_dict(test_instances["cycling2"])
    dfc = process.clean_data(df, lactate_col="lactate_8")
    di = methods.interpolate(dfc, include_baseline=False)
    logging.info(methods.determine_obla(di, 4.0))
    logging.info(methods.determine_obla(di, 2.0))
