import numpy as np
import pandas as pd
import pwlf
import statsmodels.api as sm


def lactate_data(
    df: pd.DataFrame,
    step_col: str = "step",
    length_col: str = "length",
    intensity_col: str = "intensity",
    lactate_col: str = "lactate",
    heart_rate_col: str = "heart_rate",
) -> pd.DataFrame:
    """
    Create a dataframe with the correct columns for lactate threshold analysis.
    With the new columns names "step", "length", "intensity", "lactate" and "heart_rate".
    """

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
