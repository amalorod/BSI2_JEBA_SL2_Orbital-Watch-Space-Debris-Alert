from pathlib import Path

from src.data_loader import read_csv, find_column, to_float, detect_altitude_km
from src.orbital_math import dms_to_decimal, geodetic_to_ecef, euclidean_distance_km


DATA_DIR = Path("data")
DEBRIS_FILE = DATA_DIR / "space_debris_positions.csv"
SATELLITE_FILE = DATA_DIR / "satelite_positions.csv"



def get_satellite_file() -> Path:
    if SATELLITE_FILE.exists():
        return SATELLITE_FILE
    raise FileNotFoundError("Could not find satelite_positions.csv in data folder.")


def load_debris_with_decimal_coordinates() -> list[dict]:
    debris = read_csv(DEBRIS_FILE)

    if not debris:
        return []

    first_row = debris[0]

    latitude_col = find_column(first_row, ["Lat"])
    longitude_col = find_column(first_row, ["Long"])
    

    result = []

    for row in debris:
        decimal_latitude = dms_to_decimal(row[latitude_col])
        decimal_longitude = dms_to_decimal(row[longitude_col])

        enriched = dict(row)
        enriched["decimal_latitude"] = decimal_latitude
        enriched["decimal_longitude"] = decimal_longitude

        result.append(enriched)

    return result


def load_debris_with_ecef() -> list[dict]:
    debris = load_debris_with_decimal_coordinates()

    if not debris:
        return []

    

    
    altitude_col = find_column(debris[0],  ["Alt_km"])


    result = []

    for row in debris:
        altitude_km = detect_altitude_km(row, altitude_col)

        x, y, z = geodetic_to_ecef(
            row["decimal_latitude"],
            row["decimal_longitude"],
            altitude_km
        )

        enriched = dict(row)
        enriched["altitude_km"] = altitude_km
        enriched["x"] = x
        enriched["y"] = y
        enriched["z"] = z

        result.append(enriched)

    return result


def challenge_one() -> float:
    """
    Reads debris file, converts latitude and longitude to decimal degrees,
    sums all decimal latitudes and longitudes separately and multiplies both sums.
    """
    debris = load_debris_with_decimal_coordinates()

    latitude_sum = sum(row["decimal_latitude"] for row in debris)
    longitude_sum = sum(row["decimal_longitude"] for row in debris)

    return round(latitude_sum * longitude_sum, 6)


def challenge_two() -> float:
    """
    Converts debris coordinates to ECEF and calculates the total sum of all X, Y and Z values.
    """
    debris = load_debris_with_ecef()

    total = 0.0

    for row in debris:
        total += row["x"]
        total += row["y"]
        total += row["z"]

    return round(total, 5)


def load_satellites() -> list[dict]:
    satellites = read_csv(get_satellite_file())

    if not satellites:
        return []

    first_row = satellites[0]

    x_col = find_column(first_row, ["X_m"])
    y_col = find_column(first_row, ["Y_m"])
    z_col = find_column(first_row, ["Z_m"])

    name_col = None
    for candidate in ["SatelliteID", "Name", "Satellite", "SatelliteName", "ID", "Id"]:
        try:
            name_col = find_column(first_row, [candidate])
            break
        except KeyError:
            pass

    result = []

    for index, row in enumerate(satellites, start=1):
        name = row[name_col] if name_col else f"Satellite {index}"

        x = to_float(row[x_col])
        y = to_float(row[y_col])
        z = to_float(row[z_col])

        if abs(x) > 100000 or abs(y) > 100000 or abs(z) > 100000:
            x /= 1000
            y /= 1000
            z /= 1000

        enriched = dict(row)
        enriched["satellite_name"] = name
        enriched["x"] = x
        enriched["y"] = y
        enriched["z"] = z

        result.append(enriched)

    return result


def challenge_three() -> tuple[list[dict], int]:
    """
    Finds every satellite-debris pair within 1 km.
    Returns:
    - list of collision risks
    - total distance in meters, rounded to integer
    """
    debris = load_debris_with_ecef()
    satellites = load_satellites()

    risks = []
    total_distance_m = 0.0

    for satellite in satellites:
        satellite_position = (
            satellite["x"],
            satellite["y"],
            satellite["z"]
        )

        for debris_index, debris_row in enumerate(debris, start=1):
            debris_position = (
                debris_row["x"],
                debris_row["y"],
                debris_row["z"]
            )

            distance_km = euclidean_distance_km(satellite_position, debris_position)

            if distance_km <= 1:
                distance_m = distance_km * 1000
                total_distance_m += distance_m

                risks.append({
                    "satellite": satellite["satellite_name"],
                    "debris": debris_row.get("DebrisID") or debris_row.get("Name") or debris_row.get("ID") or f"Debris {debris_index}",
                    "distance_m": round(distance_m, 2)
                })

    return risks, round(total_distance_m)