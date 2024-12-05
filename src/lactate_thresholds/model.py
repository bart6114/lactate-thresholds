import logging
from typing import List

import numpy as np
import pandas as pd
import pwlf
import statsmodels.api as sm
from numpy.polynomial.polynomial import Polynomial
from scipy.optimize import curve_fit

from lactate_thresholds.types import (
    LactateTurningPoint,
    LogLog,
    ModDMax,
)
from lactate_thresholds.utils import retrieve_heart_rate, retrieve_lactate_interpolated


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
) -> List[LactateTurningPoint]:
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

    lt1 = LactateTurningPoint(
        lactate=retrieve_lactate_interpolated(data_interpolated, breakpoint_intensities[0]),
        intensity=breakpoint_intensities[0],
        heart_rate=breakpoint_heartrates[0],
    )
    lt2 = LactateTurningPoint(
        lactate=retrieve_lactate_interpolated(data_interpolated, breakpoint_intensities[1]),
        intensity=breakpoint_intensities[1],
        heart_rate=breakpoint_heartrates[1],
    )

    return [lt1, lt2]


def determine_mod_dmax(data_clean: pd.DataFrame, data_interpolated: pd.DataFrame) -> ModDMax:
    if data_clean.empty or data_clean.iloc[0]["intensity"] == 0:
        data_dmax = data_clean.iloc[1:].copy()
    else:
        data_dmax = data_clean.copy()

    # Find the first rise in blood lactate greater than 0.4 mmol/L
    data_dmax["diffs"] = data_dmax["lactate"].diff().shift(-1)
    data_first_rise = data_dmax[data_dmax["diffs"] >= 0.4].head(1)

    if data_first_rise.empty:
        logging.warning("No first rise in blood lactate greater than 0.4 mmol/L found.")
        return None

    # Fit a 3rd degree polynomial
    def poly3(x, a, b, c, d):
        return a * x**3 + b * x**2 + c * x + d

    popt, _ = curve_fit(poly3, data_clean["intensity"], data_clean["lactate"])

    # Calculate the differences
    diff_lactate = data_dmax["lactate"].max() - data_first_rise["lactate"].values[0]
    diff_intensity = (
        data_dmax["intensity"].max() - data_first_rise["intensity"].values[0]
    )

    lin_beta = diff_lactate / diff_intensity

    # Find where the first derivative of the polynomial fit equals the slope of the line
    p = Polynomial([popt[3], popt[2], popt[1], popt[0]])
    dp = p.deriv()
    roots = (dp - lin_beta).roots()
    roots = roots[np.isreal(roots)].real
    roots = roots[roots > 0]

    max_intensity = data_dmax["intensity"].max()
    model_intensity = roots[roots <= max_intensity].max()
    model_lactate = poly3(model_intensity, *popt)

    # Workaround for unplausible estimations
    if model_lactate > 8:
        logging.warning(
            "Estimated lactate value via ModDMax is higher than 8 mmol/L. Returning None."
        )
        return None

    return ModDMax(
        lactate=retrieve_lactate_interpolated(data_interpolated, model_intensity),
        intensity=model_intensity,
        heart_rate=retrieve_heart_rate(data_clean, [model_intensity])[0],
    )


def determine_loglog(data_clean, data_interpolated, loglog_restrainer=1):
    data_filtered = data_interpolated[data_interpolated["intensity"] > 0].copy()
    data_filtered["intensity"] = np.log(data_filtered["intensity"])
    data_filtered["lactate"] = np.log(data_filtered["lactate"])

    n = len(data_filtered)
    data_filtered = data_filtered.iloc[: int(loglog_restrainer * n)]

    piecewise_fit = pwlf.PiecewiseLinFit(
        data_filtered["intensity"].values, data_filtered["lactate"].values
    )
    breakpoints = piecewise_fit.fit(2)  # 1 breakpoint means 2 segments

    loglog_intensity = np.exp(breakpoints[1])
    lactate_interpolated = retrieve_lactate_interpolated(data_interpolated, loglog_intensity)
    loglog_heart_rate = retrieve_heart_rate(data_clean, [loglog_intensity])[0]

    return LogLog(
        lactate=lactate_interpolated, intensity=loglog_intensity, heart_rate=loglog_heart_rate
    )
