import pandas as pd
import statsmodels.api as sm


def retrieve_heart_rate(df_clean, intensity_values) -> np.array:
    df_clean = df_clean.iloc[1:]

    X = sm.add_constant(df_clean["intensity"])
    y = df_clean["heart_rate"]
    model_heart_rate = sm.OLS(y, X).fit()

    new_data = pd.DataFrame({"const": 1, "intensity": intensity_values})
    return model_heart_rate.predict(new_data).round(0)

