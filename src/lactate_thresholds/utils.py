import numpy as np
import pandas as pd
import statsmodels.api as sm


def get_heart_rate(df_clean: pd.DataFrame, intensity_values: np.array) -> np.array:
    df_clean = df_clean.iloc[1:]

    X = sm.add_constant(df_clean["intensity"])
    y = df_clean["heart_rate"]
    model_heart_rate = sm.OLS(y, X).fit()

    new_data = pd.DataFrame({"const": 1, "intensity": intensity_values})
    return model_heart_rate.predict(new_data).round(0)


def get_heart_rate_interpolated(df_interpolated: pd.DataFrame, intensity: float) -> float:
    closest_intensity = df_interpolated.iloc[(df_interpolated["intensity"] - intensity).abs().argsort()[:1]]
    return closest_intensity["heart_rate"].values[0]


def get_lactate_interpolated(df_interpolated: pd.DataFrame, intensity: float) -> float:
    closest_intensity = df_interpolated.iloc[(df_interpolated["intensity"] - intensity).abs().argsort()[:1]]
    return closest_intensity["lactate"].values[0]


def get_intensity_interpolated(df_interpolated: pd.DataFrame, lactate: float) -> float:
    closest_lactate = df_interpolated.iloc[(df_interpolated["lactate"] - lactate).abs().argsort()[:1]]
    return closest_lactate["intensity"].values[0]


def get_intensity_based_on_heartrate_interpolated(df_interpolated: pd.DataFrame, heart_rate: float) -> float:
    closest_hr = df_interpolated.iloc[(df_interpolated["heart_rate"] - heart_rate).abs().argsort()[:1]]
    return closest_hr["intensity"].values[0]
