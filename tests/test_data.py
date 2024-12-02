import pandas as pd
from lactate_thresholds import process
import pytest

test_instances = {
    "simple": {
        "data": [
            {"step": 0, "length": 0, "intensity": 0, "lactate": 1.0, "heartrate": 80},
            {"step": 1, "length": 4, "intensity": 8.5, "lactate": 2.2, "heartrate": 122},
            {"step": 2, "length": 4, "intensity": 10.0, "lactate": 1.3, "heartrate": 131},
            {"step": 3, "length": 4, "intensity": 11.5, "lactate": 1.0, "heartrate": 145},
            {"step": 4, "length": 4, "intensity": 13.0, "lactate": 0.8, "heartrate": 155},
            {"step": 5, "length": 4, "intensity": 14.5, "lactate": 1.1, "heartrate": 162},
            {"step": 6, "length": 4, "intensity": 16.0, "lactate": 1.8, "heartrate": 171},
            {"step": 7, "length": 4, "intensity": 17.5, "lactate": 2.9, "heartrate": 180},
            {"step": 8, "length": 4, "intensity": 19.0, "lactate": 5.3, "heartrate": 186},
        ],
        "shouldErr": False,
    },
    "differently_named_cols": {
        "data": [
            {"step": 0, "length": 0, "intensity": 0, "lactate": 1.0, "heartrate": 80},
            {"step": 1, "length": 4, "intensity": 8.5, "lactate": 2.2, "heartrate": 122},
            {"step": 2, "length": 4, "intensity": 10.0, "lactate": 1.3, "heartrate": 131},
            {"step": 3, "length": 4, "intensity": 11.5, "lactate": 1.0, "heartrate": 145},
            {"step": 4, "length": 4, "intensity": 13.0, "lactate": 0.8, "heartrate": 155},
            {"step": 5, "length": 4, "intensity": 14.5, "lactate": 1.1, "heartrate": 162},
            {"step": 6, "length": 4, "intensity": 16.0, "lactate": 1.8, "heartrate": 171},
            {"step": 7, "length": 4, "intensity": 17.5, "lactate": 2.9, "heartrate": 180},
            {"step": 8, "length": 4, "intensity": 19.0, "lactate": 5.3, "heartrate": 186},
        ],
        "shouldErr": False,
    },
    "non_numeric_vals": {
        "data": [
            {"step": 0, "length": 0, "intensity": 0, "lactate": 1.0, "heartrate": 80},
            {"step": 1, "length": 4, "intensity": 8.5, "lactate": 2.2, "heartrate": 122},
            {"step": 2, "length": 4, "intensity": "a", "lactate": 1.3, "heartrate": 131},
            {"step": 3, "length": 4, "intensity": 11.5, "lactate": 1.0, "heartrate": 145},
            {"step": 4, "length": 4, "intensity": 13.0, "lactate": 0.8, "heartrate": 155},
            {"step": 5, "length": 4, "intensity": 14.5, "lactate": 1.1, "heartrate": 162},
            {"step": 6, "length": 4, "intensity": 16.0, "lactate": 1.8, "heartrate": 171},
            {"step": 7, "length": 4, "intensity": 17.5, "lactate": 2.9, "heartrate": 180},
            {"step": 8, "length": 4, "intensity": 19.0, "lactate": 5.3, "heartrate": 186},
        ],
        "shouldErr": False,
    },
}


@pytest.mark.parametrize("key", test_instances.keys())
def test_lactate_data_ingestion(key):
    df = pd.DataFrame.from_dict(test_instances[key]["data"])
    if test_instances[key]["shouldErr"]:
        with pytest.raises(Exception):
            process.lactate_data(df)
    else:
        process.lactate_data(df)
        # assert all needed cols are there
        assert set(df.columns) == set(["step", "length", "intensity", "lactate", "heart_rate"])


    
