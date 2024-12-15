import pandas as pd
import pytest

from lactate_thresholds import process


def test_lactate_data_ingestion_simple(test_instances):
    df = pd.DataFrame.from_dict(test_instances["simple"])
    df2 = process.clean_data(df)
    assert set(df2.columns) == set(["step", "length", "intensity", "lactate", "heart_rate"])


def test_lactate_data_ingestion_rename(test_instances):
    df = pd.DataFrame.from_dict(test_instances["differently_named_cols"])
    df2 = process.clean_data(df, heart_rate_col="heartrate", length_col="step_length")
    assert set(df2.columns) == set(["step", "length", "intensity", "lactate", "heart_rate"])

    df_cycling = pd.DataFrame.from_dict(test_instances["cycling1"])
    df2_cycling = process.clean_data(df_cycling, lactate_col="lactate_8")
    assert set(df2_cycling.columns) == set(["step", "length", "intensity", "lactate", "heart_rate"])


def test_lactate_data_ingestion_non_numeric(test_instances):
    df = pd.DataFrame.from_dict(test_instances["non_numeric_vals"])
    with pytest.raises(ValueError):
        process.clean_data(df, heart_rate_col="heartrate")


def test_should_raise_err_if_not_dataframe(test_instances):
    with pytest.raises(ValueError):
        process.clean_data(test_instances["non_numeric_vals"])
