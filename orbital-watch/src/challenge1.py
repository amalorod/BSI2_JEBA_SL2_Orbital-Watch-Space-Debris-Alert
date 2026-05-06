
from pathlib import Path

from src.data_loader import read_csv, find_column
from src.orbital_math import dms_to_decimal


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




def run_challenge_1() -> float:
    """
    Challenge 1:
    Converts latitude and longitude from DMS to decimal degrees.
    Then sums all latitudes and longitudes separately and multiplies both sums.
    """
    debris = load_debris_with_decimal_coordinates()

    latitude_sum = sum(row["decimal_latitude"] for row in debris)
    longitude_sum = sum(row["decimal_longitude"] for row in debris)

    return round(latitude_sum * longitude_sum, 6)


if __name__ == "__main__":
    result = run_challenge_1()
    print(f"Challenge 1 result: {result}")
