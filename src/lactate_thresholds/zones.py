import pandas as pd

from lactate_thresholds.types import LactateThresholdResults


def seiler_3_zones(res: LactateThresholdResults) -> pd.DataFrame:
    """Determine Seiler 3-zone training zones based on LT1 and LT2.

    Args:
        lt1 (ThresholdEstimate): Lactate threshold 1 intensity.
        lt2 (ThresholdEstimate): Lactate threshold 2 intensity.

    Returns:
        pd.DataFrame: DataFrame with Seiler 3-zone training zones, including focus and usage.
    """

    from lactate_thresholds.utils import retrieve_heart_rate_interpolated

    zone1_intensity = f"{0:.2f} - {res.lt1_estimate.intensity:.2f}"
    zone1_heartrate = f"up to {retrieve_heart_rate_interpolated(res.interpolated_data, res.lt1_estimate.intensity):.0f}"

    zone2_intensity = (
        f"{res.lt1_estimate.intensity:.2f} - {res.lt2_estimate.intensity:.2f}"
    )
    zone2_heartrate = f"{retrieve_heart_rate_interpolated(res.interpolated_data, res.lt1_estimate.intensity):.0f} - {retrieve_heart_rate_interpolated(res.interpolated_data, res.lt2_estimate.intensity):.0f}"

    zone3_intensity = f"{res.lt2_estimate.intensity:.2f} - max"
    zone3_heartrate = f"{retrieve_heart_rate_interpolated(res.interpolated_data, res.lt2_estimate.intensity):.0f} - max"

    zones = pd.DataFrame(
        {
            "zone": ["Zone 1", "Zone 2", "Zone 3"],
            "intensity": [zone1_intensity, zone2_intensity, zone3_intensity],
            "heart_rate": [zone1_heartrate, zone2_heartrate, zone3_heartrate],
            "focus": [
                "Recovery, building an aerobic foundation.",
                "Moderate aerobic work; a gray zone with limited efficiency for endurance adaptations.",
                "Enhancing anaerobic threshold and lactate tolerance.",
            ],
        }
    )

    return zones


def seiler_5_zones(res: LactateThresholdResults) -> pd.DataFrame:
    """Determine 5-zone training zones based on LT1 and LT2.

    Args:
        res (LactateThresholdResults): Object containing LT1 and LT2 estimates and interpolated data.

    Returns:
        pd.DataFrame: DataFrame with 5-zone training zones, including focus and usage.
    """

    from lactate_thresholds.utils import retrieve_heart_rate_interpolated

    lt1_intensity = res.lt1_estimate.intensity
    lt2_intensity = res.lt2_estimate.intensity

    zone1_intensity = f"0 - {0.98 * lt1_intensity:.2f}"
    zone2_intensity = f"{0.98 * lt1_intensity:.2f} - {1.02 * lt1_intensity:.2f}"
    zone3_intensity = f"{1.02 * lt1_intensity:.2f} - {0.98 * lt2_intensity:.2f}"
    zone4_intensity = f"{0.98 * lt2_intensity:.2f} - {1.02 * lt2_intensity:.2f}"
    zone5_intensity = f"{1.02 * lt2_intensity:.2f} - max"

    zone1_heartrate = f"up to {retrieve_heart_rate_interpolated(res.interpolated_data, 0.98 * lt1_intensity):.0f}"
    zone2_heartrate = f"{retrieve_heart_rate_interpolated(res.interpolated_data, 0.98 * lt1_intensity):.0f} - {retrieve_heart_rate_interpolated(res.interpolated_data, 1.02 * lt1_intensity):.0f}"
    zone3_heartrate = f"{retrieve_heart_rate_interpolated(res.interpolated_data, 1.02 * lt1_intensity):.0f} - {retrieve_heart_rate_interpolated(res.interpolated_data, 0.98 * lt2_intensity):.0f}"
    zone4_heartrate = f"{retrieve_heart_rate_interpolated(res.interpolated_data, 0.98 * lt2_intensity):.0f} - {retrieve_heart_rate_interpolated(res.interpolated_data, 1.02 * lt2_intensity):.0f}"
    zone5_heartrate = f"{retrieve_heart_rate_interpolated(res.interpolated_data, 1.02 * lt2_intensity):.0f} - max"

    zones = pd.DataFrame(
        {
            "zone": ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"],
            "intensity": [
                zone1_intensity,
                zone2_intensity,
                zone3_intensity,
                zone4_intensity,
                zone5_intensity,
            ],
            "heart_rate": [
                zone1_heartrate,
                zone2_heartrate,
                zone3_heartrate,
                zone4_heartrate,
                zone5_heartrate,
            ],
            "focus": [
                "Recovery, building an aerobic foundation.",
                "Aerobic base building and improving fat utilization.",
                "Aerobic endurance and muscular efficiency.",
                "Improving lactate tolerance and anaerobic threshold.",
                "Anaerobic capacity, speed, and power.",
            ],
        }
    )

    return zones


def friel_7_zones(res: LactateThresholdResults) -> pd.DataFrame:
    """Determine Friel's 7-zone training zones based on LTHR.

    Args:
        res (LactateThresholdResults): Object containing LT2 estimate and interpolated data.

    Returns:
        pd.DataFrame: DataFrame with Friel's 7-zone training zones.
    """
    from lactate_thresholds.utils import (
        retrieve_intensity_based_on_heartrate_interpolated,
    )

    lt2_heart_rate = res.lt2_estimate.heart_rate

    hr_zone1 = 0.85 * lt2_heart_rate
    hr_zone2 = 0.89 * lt2_heart_rate
    hr_zone3 = 0.94 * lt2_heart_rate
    hr_zone4 = 0.99 * lt2_heart_rate
    hr_zone5a = 1.02 * lt2_heart_rate
    hr_zone5b = 1.06 * lt2_heart_rate

    zones = pd.DataFrame(
        {
            "zone": [
                "Zone 1",
                "Zone 2",
                "Zone 3",
                "Zone 4",
                "Zone 5a",
                "Zone 5b",
                "Zone 5c",
            ],
            "heart_rate": [
                f"Less than {hr_zone1:.0f}",
                f"{hr_zone1:.0f} - {hr_zone2:.0f}",
                f"{hr_zone2:.0f} - {hr_zone3:.0f}",
                f"{hr_zone3:.0f} - {hr_zone4:.0f}",
                f"{hr_zone4:.0f} - {hr_zone5a:.0f}",
                f"{hr_zone5a:.0f} - {hr_zone5b:.0f}",
                f"More than {hr_zone5b:.0f}",
            ],
            "intensity": [
                f"Less than {retrieve_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone1):.2f}",
                f"{retrieve_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone1):.2f} - {retrieve_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone2):.2f}",
                f"{retrieve_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone2):.2f} - {retrieve_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone3):.2f}",
                f"{retrieve_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone3):.2f} - {retrieve_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone4):.2f}",
                f"{retrieve_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone4):.2f} - {retrieve_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone5a):.2f}",
                f"{retrieve_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone5a):.2f} - {retrieve_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone5b):.2f}",
                f"More than {retrieve_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone5b):.2f}",
            ],
            "focus": [
                "Active recovery, very easy efforts.",
                "Aerobic base building and endurance.",
                "Improving aerobic capacity and stamina.",
                "Threshold training, preparing for race pace.",
                "VO2 max improvement and anaerobic tolerance.",
                "Improving power and anaerobic endurance.",
                "Maximum effort for peak performance.",
            ],
        }
    )

    return zones
