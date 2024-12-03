import pandas as pd
import pytest

from lactate_thresholds import model, process


def test_interpolation(test_instances):
    ld = pd.DataFrame.from_dict(test_instances["simple"])
    df = process.lactate_data(ld)
    idf = model.interpolate(df)
