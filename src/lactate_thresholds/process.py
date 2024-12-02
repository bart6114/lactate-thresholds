import numpy as np
import pandas as pd
from numpy.polynomial.polynomial import Polynomial


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


def interpolate(df: pd.DataFrame, interpolation_factor: float = 0.001) -> pd.DataFrame:
    """
    Interpolates a new dataset using a 3rd degree polynomial method.

    Parameters:
    df (pd.DataFrame): The input dataframe with columns 'intensity' and 'lactate'.
    interpolation_factor (float): The factor for interpolation. Default is 0.001.

    Returns:
    pd.DataFrame: The interpolated dataframe.
    """

    # Sort the dataframe by intensity
    df = df.sort_values(by="intensity")

    # Fit a 3rd degree polynomial to the data
    p = Polynomial.fit(df["intensity"], df["lactate"], 3)

    # Create new intensity values for interpolation
    new_intensity = np.arange(
        df["intensity"].min(), df["intensity"].max(), interpolation_factor
    )

    # Evaluate the polynomial at the new intensity values
    new_lactate = p(new_intensity)

    # Create a new dataframe with the interpolated values
    interpolated_df = pd.DataFrame({"intensity": new_intensity, "lactate": new_lactate})

    return interpolated_df
