import pandas as pd

from lactate_thresholds.types import ThresholdEstimate


def seiler_3_zones(lt1: ThresholdEstimate, lt2: ThresholdEstimate) -> pd.DataFrame:
    """Determine Seiler 3-zone training zones based on LT1 and LT2.

    Args:
        lt1 (ThresholdEstimate): Lactate threshold 1 intensity.
        lt2 (ThresholdEstimate): Lactate threshold 2 intensity.

    Returns:
        pd.DataFrame: DataFrame with Seiler 3-zone training zones, including focus and usage.
    """

    zones = pd.DataFrame(
        {
            "zone": ["Zone 1", "Zone 2", "Zone 3"],
            "intensity": [
                f"0 - {round(lt1.intensity, 1)}",
                f"{round(lt1.intensity, 1)} - {round(lt2.intensity, 1)}",
                f"{round(lt2.intensity, 1)} - max",
            ],
            "heart_rate": [
                f"up to {round(lt1.heart_rate)}",
                f"{round(lt1.heart_rate)} - {round(lt2.heart_rate)}",
                f"{round(lt2.heart_rate)} - max",
            ],
            "focus": [
                "Recovery, building an aerobic foundation.",
                "Moderate aerobic work; a gray zone with limited efficiency for endurance adaptations.",
                "Enhancing anaerobic threshold and lactate tolerance.",
            ],
            "usage": [
                "Active recovery, very easy runs.",
                "Occasional steady-state runs; not the focus of polarized training.",
                "Interval training, threshold runs, or race pace efforts.",
            ],
        }
    )

    return zones


def seiler_5_zones(lt1: ThresholdEstimate, lt2: ThresholdEstimate) -> pd.DataFrame:
    """Determine 5-zone training zones based on LT1 and LT2.

    Args:
        lt1 (ThresholdEstimate): Lactate threshold 1 intensity.
        lt2 (ThresholdEstimate): Lactate threshold 2 intensity.

    Returns:
        pd.DataFrame: DataFrame with 5-zone training zones.
    """

    zones = pd.DataFrame(
        {
            "zone": ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"],
            "intensity": [
                f"0 - {0.98 * lt1.intensity:.2f}",
                f"{0.98 * lt1.intensity:.2f} - {1.02 * lt1.intensity:.2f}",
                f"{1.02 * lt1.intensity:.2f} - {0.98 * lt2.intensity:.2f}",
                f"{0.98 * lt2.intensity:.2f} - {1.02 * lt2.intensity:.2f}",
                f"{1.02 * lt2.intensity:.2f} - max",
            ],
            "heart_rate": [
                f"up to {0.98 * lt1.heart_rate:.0f}",
                f"{0.98 * lt1.heart_rate:.0f} - {1.02 * lt1.heart_rate:.0f}",
                f"{1.02 * lt1.heart_rate:.0f} - {0.98 * lt2.heart_rate:.0f}",
                f"{0.98 * lt2.heart_rate:.0f} - {1.02 * lt2.heart_rate:.0f}",
                f"{1.02 * lt2.heart_rate:.0f} - max",
            ],
            "focus": [
                "Recovery, building an aerobic foundation.",
                "Aerobic base building and improving fat utilization.",
                "Aerobic endurance and muscular efficiency.",
                "Improving lactate tolerance and anaerobic threshold.",
                "Anaerobic capacity, speed, and power.",
            ],
            "usage": [
                "Active recovery, very easy runs.",
                "Long, steady endurance runs.",
                "Tempo runs or sustained threshold-like efforts.",
                "Interval training, threshold runs, or race-pace efforts.",
                "High-intensity intervals, VO2 max efforts, or sprints.",
            ],
        }
    )

    return zones
