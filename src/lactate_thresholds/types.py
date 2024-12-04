import pandas as pd
from pydantic import BaseModel, ConfigDict


class BaseMeasurement(BaseModel):
    lactate: float
    intensity: float
    heart_rate: float


class LactateTurningPoint(BaseMeasurement):
    pass


class ModDMax(BaseMeasurement):
    pass


class LactateThresholdResults(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    clean_data: pd.DataFrame
    interpolated_data: pd.DataFrame
    ltp1: LactateTurningPoint | None = None
    ltp2: LactateTurningPoint | None = None
    mod_dmax: ModDMax | None = None
