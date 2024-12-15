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

    from lactate_thresholds.utils import get_heart_rate_interpolated

    zone1_intensity = f"{0:.2f} - {res.lt1_estimate.intensity:.2f}"
    zone1_heartrate = f"up to {get_heart_rate_interpolated(res.interpolated_data, res.lt1_estimate.intensity):.0f}"

    zone2_intensity = f"{res.lt1_estimate.intensity:.2f} - {res.lt2_estimate.intensity:.2f}"
    zone2_heartrate = (
        f"{get_heart_rate_interpolated(res.interpolated_data, res.lt1_estimate.intensity):.0f} - "
        f"{get_heart_rate_interpolated(res.interpolated_data, res.lt2_estimate.intensity):.0f}"
    )

    zone3_intensity = f"{res.lt2_estimate.intensity:.2f} - max"
    zone3_heartrate = f"{get_heart_rate_interpolated(res.interpolated_data, res.lt2_estimate.intensity):.0f} - max"

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

    from lactate_thresholds.utils import get_heart_rate_interpolated

    lt1_intensity = res.lt1_estimate.intensity
    lt2_intensity = res.lt2_estimate.intensity

    zone1_intensity = f"0 - {0.98 * lt1_intensity:.2f}"
    zone2_intensity = f"{0.98 * lt1_intensity:.2f} - {1.02 * lt1_intensity:.2f}"
    zone3_intensity = f"{1.02 * lt1_intensity:.2f} - {0.98 * lt2_intensity:.2f}"
    zone4_intensity = f"{0.98 * lt2_intensity:.2f} - {1.02 * lt2_intensity:.2f}"
    zone5_intensity = f"{1.02 * lt2_intensity:.2f} - max"

    zone1_heartrate = f"up to {get_heart_rate_interpolated(res.interpolated_data, 0.98 * lt1_intensity):.0f}"
    zone2_heartrate = (
        f"{get_heart_rate_interpolated(res.interpolated_data, 0.98 * lt1_intensity):.0f} - "
        f"{get_heart_rate_interpolated(res.interpolated_data, 1.02 * lt1_intensity):.0f}"
    )
    zone3_heartrate = (
        f"{get_heart_rate_interpolated(res.interpolated_data, 1.02 * lt1_intensity):.0f} - "
        f"{get_heart_rate_interpolated(res.interpolated_data, 0.98 * lt2_intensity):.0f}"
    )
    zone4_heartrate = (
        f"{get_heart_rate_interpolated(res.interpolated_data, 0.98 * lt2_intensity):.0f} - "
        f"{get_heart_rate_interpolated(res.interpolated_data, 1.02 * lt2_intensity):.0f}"
    )
    zone5_heartrate = f"{get_heart_rate_interpolated(res.interpolated_data, 1.02 * lt2_intensity):.0f} - max"

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


# friel references
# https://web.archive.org/web/20241212065559/https://www.trainingbible.com/joesblog/2009/11/quick-guide-to-setting-zones.html


def friel_7_zones_running(res: LactateThresholdResults) -> pd.DataFrame:
    """Determine Friel's 7-zone training zones based on LT (Lactate Threshold).

    Args:
        res (LactateThresholdResults): Object containing LT2 estimate and interpolated data.

    Returns:
        pd.DataFrame: DataFrame with Friel's 7-zone training zones.
    """
    from lactate_thresholds.utils import (
        get_intensity_based_on_heartrate_interpolated,
    )

    lt2_heart_rate = res.lt2_estimate.heart_rate

    # Define zone boundaries based on LT2
    hr_zone1 = [0, 0.85 * lt2_heart_rate]
    hr_zone2 = [0.85 * lt2_heart_rate, 0.89 * lt2_heart_rate]
    hr_zone3 = [0.90 * lt2_heart_rate, 0.94 * lt2_heart_rate]
    hr_zone4 = [0.95 * lt2_heart_rate, 0.99 * lt2_heart_rate]
    hr_zone5a = [1.00 * lt2_heart_rate, 1.02 * lt2_heart_rate]
    hr_zone5b = [1.03 * lt2_heart_rate, 1.06 * lt2_heart_rate]
    hr_zone5c = [1.06 * lt2_heart_rate, res.clean_data.heart_rate.max()]

    # Create the zones DataFrame
    zones = pd.DataFrame(
        {
            "zone": [
                "Zone 1. Recovery",
                "Zone 2. Aerobic",
                "Zone 3. Tempo",
                "Zone 4. SubThreshold",
                "Zone 5a. VO2 SuperThreshold",
                "Zone 5b. Aerobic Capacity",
                "Zone 5c. Anaerobic Capacity",
            ],
            "intensity": [
                f"up to {get_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone1[1]):.2f}",
                f"{get_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone2[0]):.2f} - "
                f"{get_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone2[1]):.2f}",
                f"{get_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone3[0]):.2f} - "
                f"{get_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone3[1]):.2f}",
                f"{get_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone4[0]):.2f} - "
                f"{get_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone4[1]):.2f}",
                f"{get_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone5a[0]):.2f} - "
                f"{get_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone5a[1]):.2f}",
                f"{get_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone5b[0]):.2f} - "
                f"{get_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone5b[1]):.2f}",
                f"more than {get_intensity_based_on_heartrate_interpolated(res.interpolated_data, hr_zone5c[0]):.2f}",
            ],
            "heart_rate": [
                f"{hr_zone1[0]:.0f} - {hr_zone1[1]:.0f}",
                f"{hr_zone2[0]:.0f} - {hr_zone2[1]:.0f}",
                f"{hr_zone3[0]:.0f} - {hr_zone3[1]:.0f}",
                f"{hr_zone4[0]:.0f} - {hr_zone4[1]:.0f}",
                f"{hr_zone5a[0]:.0f} - {hr_zone5a[1]:.0f}",
                f"{hr_zone5b[0]:.0f} - {hr_zone5b[1]:.0f}",
                f"{hr_zone5c[0]:.0f} - max",
            ],
            "focus": [
                "Active recovery.",
                "Aerobic endurance.",
                "Building aerobic capacity and stamina.",
                "Threshold effort.",
                "Improving VO2 max.",
                "Anaerobic capacity.",
                "Peak power output.",
            ],
        }
    )

    return zones
