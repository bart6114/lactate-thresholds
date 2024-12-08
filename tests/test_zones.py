import logging

import pandas as pd

from lactate_thresholds import determine, methods, process
from lactate_thresholds.zones import seiler_3_zones, seiler_5_zones


def test_seiler_zones(test_instances):
    df = pd.DataFrame.from_dict(test_instances["cycling2"])
    r = determine(df, lactate_col="lactate_8")

    zones = seiler_3_zones(r.lt1_estimate, r.lt2_estimate)
    logging.info(zones)
    zones = seiler_5_zones(r.lt1_estimate, r.lt2_estimate)
    logging.info(zones)
