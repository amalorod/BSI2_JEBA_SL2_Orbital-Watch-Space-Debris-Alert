import math
import re


WGS84_A_KM = 6378.137
WGS84_E2 = (1 / 298.257223563) * (2 - 1 / 298.257223563)


def dms_to_decimal(value: str) -> float:
    """
    Converts a GPS coordinate in degree-minute-second format to decimal degrees.

    Example:
    11°37'44N -> 11.628889
    145°50'21W -> -145.839167
    """
    if value is None:
        raise ValueError("Coordinate value is missing.")

    text = str(value).strip().upper()

    pattern = r"(\d+)[°\s]+(\d+)['\s]+(\d+(?:\.\d+)?)[\"\s]*([NSEW])"
    match = re.search(pattern, text)

    if not match:
        raise ValueError(f"Invalid DMS coordinate format: {value}")

    degrees = float(match.group(1))
    minutes = float(match.group(2))
    seconds = float(match.group(3))
    direction = match.group(4)

    decimal = degrees + minutes / 60 + seconds / 3600

    if direction in ("S", "W"):
        decimal *= -1

    return round(decimal, 6)


def geodetic_to_ecef(latitude_deg: float, longitude_deg: float, altitude_km: float) -> tuple[float, float, float]:
    """
    Converts geodetic coordinates to ECEF coordinates.

    Input:
    - latitude in decimal degrees
    - longitude in decimal degrees
    - altitude in kilometers

    Output:
    - x, y, z in kilometers
    """
    lat = math.radians(latitude_deg)
    lon = math.radians(longitude_deg)

    sin_lat = math.sin(lat)
    cos_lat = math.cos(lat)

    n = WGS84_A_KM / math.sqrt(1 - WGS84_E2 * sin_lat * sin_lat)

    x = (n + altitude_km) * cos_lat * math.cos(lon)
    y = (n + altitude_km) * cos_lat * math.sin(lon)
    z = (n * (1 - WGS84_E2) + altitude_km) * sin_lat

    return x,y,z


def euclidean_distance_km(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    """
    Calculates the Euclidean distance between two 3D points in kilometers.
    """
    return math.sqrt(
        (a[0] - b[0]) ** 2
        + (a[1] - b[1]) ** 2
        + (a[2] - b[2]) ** 2
    )