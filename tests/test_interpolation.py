import pandas as pd
import pytest

from lactate_thresholds import process

test_instances = {
    "simple": [
        {"step": 0, "length": 0, "intensity": 0, "lactate": 1.0, "heart_rate": 80},
        {"step": 1, "length": 4, "intensity": 8.5, "lactate": 2.2, "heart_rate": 122},
        {"step": 2, "length": 4, "intensity": 10.0, "lactate": 1.3, "heart_rate": 131},
        {"step": 3, "length": 4, "intensity": 11.5, "lactate": 1.0, "heart_rate": 145},
        {"step": 4, "length": 4, "intensity": 13.0, "lactate": 0.8, "heart_rate": 155},
        {"step": 5, "length": 4, "intensity": 14.5, "lactate": 1.1, "heart_rate": 162},
        {"step": 6, "length": 4, "intensity": 16.0, "lactate": 1.8, "heart_rate": 171},
        {"step": 7, "length": 4, "intensity": 17.5, "lactate": 2.9, "heart_rate": 180},
        {"step": 8, "length": 4, "intensity": 19.0, "lactate": 5.3, "heart_rate": 186},
    ]
}


def test_interpolation():
    ld = pd.DataFrame.from_dict(test_instances["simple"])
    idf = process.interpolate(ld)
