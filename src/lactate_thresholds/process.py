import numpy as np
import pandas as pd
import pwlf
import statsmodels.api as sm

from lactate_thresholds.model import determine_ltp, interpolate


def clean_data(
    df: pd.DataFrame,
    step_col: str = "step",
    length_col: str = "length",
    intensity_col: str = "intensity",
    lactate_col: str = "lactate",
    heart_rate_col: str = "heart_rate",
) -> pd.DataFrame:
    
    ## if df not a dataframe raise valueerror
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input is not a DataFrame")

    df_clean = df.copy()
    df_clean = df_clean.rename(
        columns={
            step_col: "step",
            length_col: "length",
            intensity_col: "intensity",
            lactate_col: "lactate",
            heart_rate_col: "heart_rate",
        }
    )
    df_clean = df_clean[["step", "length", "intensity", "lactate", "heart_rate"]]

    ## iterate over columns and assert that all entries in the column are numeric
    for col in df_clean.columns:
        if not pd.api.types.is_numeric_dtype(df_clean[col]):
            raise ValueError(
                f"Column '{col}' is not numeric / contains nonnumeric values"
            )

    return df_clean


def determine(df: pd.DataFrame,
    step_col: str = "step",
    length_col: str = "length",
    intensity_col: str = "intensity",
    lactate_col: str = "lactate",
    heart_rate_col: str = "heart_rate", include_baseline = False) -> pd.DataFrame:

    dfc = clean_data(df, step_col, length_col, intensity_col, lactate_col, heart_rate_col)
    dfi = interpolate(dfc, include_baseline=include_baseline)

    return determine_ltp(dfc, dfi)
    
