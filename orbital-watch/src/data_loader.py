import csv
from pathlib import Path


def read_csv(path: str | Path) -> list[dict]:
    """
    Reads a CSV file and returns a list of dictionaries.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)


def find_column(row: dict, possible_names: list[str]) -> str:
    """
    Finds a column in a CSV row by checking possible names case-insensitively.
    """
    normalized = {key.lower().strip(): key for key in row.keys()}

    for name in possible_names:
        key = name.lower().strip()
        if key in normalized:
            return normalized[key]

    available = ", ".join(row.keys())
    raise KeyError(f"Could not find one of {possible_names}. Available columns: {available}")


def to_float(value) -> float:
    """
    Converts a CSV value to float and handles decimal commas.
    """
    return float(str(value).strip().replace(",", "."))


def detect_altitude_km(row: dict, altitude_column: str) -> float:
    """
    Tries to detect whether altitude is stored in meters or kilometers.
    If the column name contains 'm' but not 'km', it assumes meters.
    If the value is very large, it also assumes meters.
    """
    raw_value = to_float(row[altitude_column])
    column_name = altitude_column.lower()

    if "km" in column_name:
        return raw_value

    if "meter" in column_name or column_name.endswith("_m") or column_name.endswith(" m"):
        return raw_value / 1000

    if abs(raw_value) > 10000:
        return raw_value / 1000

    return raw_value