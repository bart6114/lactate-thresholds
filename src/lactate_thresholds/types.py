import pandas as pd
from pydantic import BaseModel, ConfigDict


class LactateThresholdPoint(BaseModel):
    lactate: float
    intensity: float
    heart_rate: float


class LactateThresholdResults(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    clean_data: pd.DataFrame
    interpolated_data: pd.DataFrame
    ltp1: LactateThresholdPoint
    ltp2: LactateThresholdPoint

