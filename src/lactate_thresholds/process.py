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

import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

def interpolate(
    df: pd.DataFrame,
    interpolation_factor: float = 0.1,
    include_baseline: bool = True
) -> pd.DataFrame:
    """
    Interpolates a new dataset using a 3rd-degree polynomial regression model.

    Parameters:
    df (pd.DataFrame): The input dataframe with columns 'intensity' and 'lactate'.
    interpolation_factor (float): The step size for interpolation. Default is 0.1.
    include_baseline (bool): Whether to include the baseline value.

    Returns:
    pd.DataFrame: The interpolated dataframe with new intensity and lactate values.
    """
    # Adjust baseline intensity
    if include_baseline and (df['intensity'] == 0).any():
        to_subtract = df.iloc[2]['intensity'] - df.iloc[1]['intensity']
        df.loc[df['intensity'] == 0, 'intensity'] = df.iloc[1]['intensity'] - to_subtract

    # Remove baseline if not included
    if not include_baseline and (df['intensity'] == 0).any():
        df = df[df['intensity'] != 0]

    # Sort the dataframe by intensity
    df = df.sort_values(by="intensity").reset_index(drop=True)

    # Create a pipeline for polynomial regression
    model = make_pipeline(PolynomialFeatures(degree=3, include_bias=False), LinearRegression())

    # Fit the model
    model.fit(df[["intensity"]], df["lactate"])

    # Generate new intensity values for interpolation
    new_intensity = pd.DataFrame(
        np.arange(df["intensity"].min(), df["intensity"].max(), interpolation_factor),
        columns=["intensity"]
    )

    # Predict lactate values for the new intensity data
    new_lactate = model.predict(new_intensity)

    # Combine interpolated values into a new DataFrame
    interpolated_df = pd.DataFrame({
        "intensity": new_intensity["intensity"],
        "lactate": new_lactate
    })
    interpolated_df.to_clipboard(excel=True)

    return interpolated_df
import pandas as pd
import pwlf
import numpy as np


def determine_ltp(data_clean: pd.DataFrame, data_interpolated: pd.DataFrame, n_breakpoints: int = 2) -> pd.DataFrame:
    """
    Determine lactate turning points (LTP) using piecewise linear regression.

    Parameters:
    - data_interpolated (pd.DataFrame): DataFrame with 'intensity' and 'lactate' columns.
    - n_breakpoints (int): Number of breakpoints to determine.

    Returns:
    - pd.DataFrame: DataFrame with method, fitting, intensity, and lactate values.
    """


    # Extract intensity and lactate data
    X = data_interpolated['intensity'].values
    y = data_interpolated['lactate'].values

    # Validate sufficient data for breakpoints
    if len(X) <= n_breakpoints:
        raise ValueError(f"Not enough data points to determine {n_breakpoints} breakpoints.")

    # Fit piecewise linear model
    pwlf_model = pwlf.PiecewiseLinFit(X, y)
    breakpoints = pwlf_model.fit(n_breakpoints + 1)  # n_segments = n_breakpoints + 1

    # Get breakpoint intensities and corresponding lactate values
    breakpoint_intensities = breakpoints[1:-1]  # Ignore first and last points
    breakpoint_lactates = pwlf_model.predict(breakpoint_intensities)

    # Build result DataFrame
    result = pd.DataFrame({
        'method': [f'LTP{i + 1}' for i in range(len(breakpoint_intensities))],
        'fitting': 'Piecewise Linear Fit',
        'intensity': breakpoint_intensities,
        'lactate': breakpoint_lactates,
        'heart_rate': [retrieve_heart_rate(data_clean, intensity) for intensity in breakpoint_intensities]
    })

    return result


import pandas as pd
import statsmodels.api as sm

def retrieve_heart_rate(df_clean, intensity_value):
    df_clean = df_clean.iloc[1:]

    X = sm.add_constant(df_clean['intensity'])
    y = df_clean['heart_rate']
    model_heart_rate = sm.OLS(y, X).fit()

    
    new_data = pd.DataFrame({'const': 1, 'intensity': [intensity_value]})
    out = model_heart_rate.predict(new_data)

    out = round(out.iloc[0], 0)

    return out