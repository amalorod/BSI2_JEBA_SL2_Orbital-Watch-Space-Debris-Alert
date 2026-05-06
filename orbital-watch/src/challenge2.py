
from src.data_loader import find_column, detect_altitude_km
from src.orbital_math import geodetic_to_ecef
from src.challenge1 import load_debris_with_decimal_coordinates


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




def run_challenge_2() -> float:
    """
    Challenge 2:
    Converts debris GPS coordinates to ECEF and sums all X, Y and Z values.
    """
    debris = load_debris_with_ecef()

    total = 0.0

    for row in debris:
        total += row["x"]
        total += row["y"]
        total += row["z"]

    return round(total, 5)


if __name__ == "__main__":
    result = run_challenge_2()
    print(f"Challenge 2 result: {result}")
