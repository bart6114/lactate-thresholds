import logging

import pandas as pd

from lactate_thresholds import determine
from lactate_thresholds.zones import (
    friel_7_zones_running,
    seiler_3_zones,
    seiler_5_zones,
)

col_set = ["zone", "intensity", "heart_rate", "focus"]


def test_seiler_zones(test_instances):
    df = pd.DataFrame.from_dict(test_instances["cycling2"])
    r = determine(df, lactate_col="lactate_8")

    zones = seiler_3_zones(r)
    assert list(zones.columns) == col_set

    logging.info(zones)
    zones = seiler_5_zones(r)
    assert list(zones.columns) == col_set
    logging.info(zones)


def test_friel_zones(test_instances):
    df = pd.DataFrame.from_dict(test_instances["cycling2"])
    r = determine(df, lactate_col="lactate_8")

    zones = friel_7_zones_running(r)
    assert list(zones.columns) == col_set
    logging.info(zones)
