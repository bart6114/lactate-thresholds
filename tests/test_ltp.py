import pandas as pd

from lactate_thresholds import process

def test_interpolation(test_instances):
    df = pd.DataFrame.from_dict(test_instances["simple"])
    dfc = process.lactate_data(df)
    dfi = process.interpolate(dfc, include_baseline=False)
    print(process.determine_ltp(dfc, dfi))
