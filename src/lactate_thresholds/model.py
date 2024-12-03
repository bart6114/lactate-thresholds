import numpy as np
import pandas as pd
import pwlf
import statsmodels.api as sm

from lactate_thresholds.types import LactateThresholdPoint, LactateThresholdResults
from lactate_thresholds.utils import retrieve_heart_rate


def interpolate(
    df: pd.DataFrame, interpolation_factor: float = 0.1, include_baseline: bool = True
) -> pd.DataFrame:
    """
    Interpolates a new dataset using a 3rd-degree polynomial regression model (statsmodels).

    Parameters:
    df (pd.DataFrame): The input dataframe with columns 'intensity' and 'lactate'.
    interpolation_factor (float): The step size for interpolation. Default is 0.1.
    include_baseline (bool): Whether to include the baseline value.

    Returns:
    pd.DataFrame: The interpolated dataframe with new intensity and lactate values.
    """
    # Adjust baseline intensity
    if include_baseline and (df["intensity"] == 0).any():
        to_subtract = df.iloc[2]["intensity"] - df.iloc[1]["intensity"]
        df.loc[df["intensity"] == 0, "intensity"] = (
            df.iloc[1]["intensity"] - to_subtract
        )

    # Remove baseline if not included
    if not include_baseline and (df["intensity"] == 0).any():
        df = df[df["intensity"] != 0]

    # Sort the dataframe by intensity
    df = df.sort_values(by="intensity").reset_index(drop=True)

    # Create polynomial features manually
    X = np.column_stack([df["intensity"] ** i for i in range(1, 4)])  # 3rd degree
    y = df["lactate"]

    # Fit the statsmodels OLS model
    X = sm.add_constant(X)  # Add intercept term
    model = sm.OLS(y, X).fit()

    # Generate new intensity values for interpolation
    new_intensity = np.arange(
        df["intensity"].min(), df["intensity"].max(), interpolation_factor
    )
    new_X = np.column_stack([new_intensity**i for i in range(1, 4)])
    new_X = sm.add_constant(new_X)  # Add intercept term for prediction

    # Predict lactate values for the new intensity data
    new_lactate = model.predict(new_X)

    # Combine interpolated values into a new DataFrame
    interpolated_df = pd.DataFrame({"intensity": new_intensity, "lactate": new_lactate})

    return interpolated_df


def determine_ltp(
    data_clean: pd.DataFrame, data_interpolated: pd.DataFrame, n_breakpoints: int = 2
) -> pd.DataFrame:
    # Extract intensity and lactate data
    X = data_interpolated["intensity"].values
    y = data_interpolated["lactate"].values

    # Fit piecewise linear model
    pwlf_model = pwlf.PiecewiseLinFit(X, y)
    breakpoints = pwlf_model.fit(n_breakpoints + 1)  # n_segments = n_breakpoints + 1

    # Get breakpoint intensities and corresponding lactate values
    breakpoint_intensities = breakpoints[1:-1]  # Ignore first and last points
    breakpoint_lactates = pwlf_model.predict(breakpoint_intensities)
    breakpoint_heartrates = retrieve_heart_rate(data_clean, breakpoint_intensities)

    lt1 = LactateThresholdPoint(
        lactate=breakpoint_lactates[0],
        intensity=breakpoint_intensities[0],
        heart_rate=breakpoint_heartrates[0],
    )
    lt2 = LactateThresholdPoint(
        lactate=breakpoint_lactates[1],
        intensity=breakpoint_intensities[1],
        heart_rate=breakpoint_heartrates[1],
    )

    return LactateThresholdResults(
        clean_data=data_clean, interpolated_data=data_interpolated, ltp1=lt1, ltp2=lt2
    )
