
from pathlib import Path

from src.data_loader import read_csv, find_column, to_float
from src.orbital_math import euclidean_distance_km
from src.challenge2 import load_debris_with_ecef


DATA_DIR = Path("data")
SATELLITE_FILE = DATA_DIR / "satelite_positions.csv"



def get_satellite_file() -> Path:
    if SATELLITE_FILE.exists():
        return SATELLITE_FILE

    raise FileNotFoundError("Could not find satelite_positions.csv in data folder.")


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

        # Satellite coordinates are stored in meters, but debris ECEF uses kilometers.
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


def run_challenge_3() -> tuple[list[dict], int]:
    """
    Challenge 3:
    Finds all satellite-debris pairs with a distance of 1 km or less.
    Returns the risks and the total distance in meters.
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
                    "debris": debris_row.get("DebrisID") or f"Debris {debris_index}",
                    "distance_m": round(distance_m, 2)
                })

    return risks, round(total_distance_m)


if __name__ == "__main__":
    risks, total_distance_m = run_challenge_3()

    print(f"Challenge 3 collision risks: {len(risks)}")
    print(f"Challenge 3 total distance: {total_distance_m} m")

    if risks:
        print()
        print("Detected risks:")
        for risk in risks:
            print(
                f"- {risk['satellite']} near {risk['debris']}: "
                f"{risk['distance_m']} m"
            )
