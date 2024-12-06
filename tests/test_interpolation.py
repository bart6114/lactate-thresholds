import pandas as pd

from lactate_thresholds import methods, process


def test_interpolation(test_instances):
    ld = pd.DataFrame.from_dict(test_instances["simple"])
    df = process.clean_data(ld)
    idf = methods.interpolate(df)
