from __future__ import annotations
from pathlib import Path
from time import perf_counter

from src.data_loader import read_csv, find_column, to_float
from src.kd_tree import KDTreeNode, build_kd_tree, radius_search
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


def _build_debris_kd_tree(debris: list[dict]) -> "KDTreeNode" | None:
    points = [
        (
            (row["x"], row["y"], row["z"]),
            (row, debris_index)
        )
        for debris_index, row in enumerate(debris, start=1)
    ]
    return build_kd_tree(points)

def run_challenge_3_kd_tree() -> tuple[list[dict], int]:
    debris = load_debris_with_ecef()
    satellites = load_satellites()

    debris_points = []

    for index, debris_row in enumerate(debris, start=1):
        point = (
            debris_row["x"],
            debris_row["y"],
            debris_row["z"]
        )

        payload = {
            "debris": debris_row.get("DebrisID") or f"Debris {index}"
        }

        debris_points.append((point, payload))

    tree = build_kd_tree(debris_points)

    risks = []
    total_distance_m = 0.0

    for satellite in satellites:
        satellite_position = (
            satellite["x"],
            satellite["y"],
            satellite["z"]
        )

        matches = radius_search(tree, satellite_position, 1)

        for payload, distance_km in matches:
            distance_m = distance_km * 1000
            total_distance_m += distance_m

            risks.append({
                "satellite": satellite["satellite_name"],
                "debris": payload["debris"],
                "distance_m": round(distance_m, 2)
            })

    return risks, round(total_distance_m)




def run_challenge_3() -> tuple[list[dict], int]:
    brute_force_risks, brute_force_total = run_challenge_3_brute_force()
    kd_tree_risks, kd_tree_total = run_challenge_3_kd_tree()

    if brute_force_total != kd_tree_total or len(brute_force_risks) != len(kd_tree_risks):
        print("Warning: Brute force and KD-tree results differ.")

    return kd_tree_risks, kd_tree_total


def _find_collision_risks_bruteforce(debris: list[dict], satellites: list[dict]) -> tuple[list[dict], int]:
    risks = []
    total_distance_m = 0.0

    for satellite in satellites:
        satellite_position = (satellite["x"], satellite["y"], satellite["z"])

        for debris_index, debris_row in enumerate(debris, start=1):
            debris_position = (debris_row["x"], debris_row["y"], debris_row["z"])
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


def _find_collision_risks_kd_tree(debris: list[dict], satellites: list[dict]) -> tuple[list[dict], int]:
    tree = _build_debris_kd_tree(debris)
    risks = []
    total_distance_m = 0.0

    for satellite in satellites:
        satellite_position = (satellite["x"], satellite["y"], satellite["z"])
        neighbors = radius_search(tree, satellite_position, 1.0)

        for (debris_row, debris_index), distance_km in neighbors:
            distance_m = distance_km * 1000
            total_distance_m += distance_m
            risks.append({
                "satellite": satellite["satellite_name"],
                "debris": debris_row.get("DebrisID") or f"Debris {debris_index}",
                "distance_m": round(distance_m, 2)
            })

    return risks, round(total_distance_m)


def run_challenge_3_brute_force() -> tuple[list[dict], int]:
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


def run_challenge_3(use_kd_tree: bool = True) -> tuple[list[dict], int]:
    """
    Challenge 3:
    Finds all satellite-debris pairs with a distance of 1 km or less.
    Returns the risks and the total distance in meters.

    By default, this uses the faster k-d tree implementation.
    """
    debris = load_debris_with_ecef()
    satellites = load_satellites()

    if use_kd_tree:
        return _find_collision_risks_kd_tree(debris, satellites)

    return _find_collision_risks_bruteforce(debris, satellites)


def compare_challenge_3_methods() -> tuple[tuple[list[dict], int], tuple[list[dict], int], float, float]:
    debris = load_debris_with_ecef()
    satellites = load_satellites()

    start = perf_counter()
    brute_risks, brute_total = _find_collision_risks_bruteforce(debris, satellites)
    brute_duration = perf_counter() - start

    start = perf_counter()
    kd_risks, kd_total = _find_collision_risks_kd_tree(debris, satellites)
    kd_duration = perf_counter() - start

    return (brute_risks, brute_total), (kd_risks, kd_total), brute_duration, kd_duration


if __name__ == "__main__":
    (brute_risks, brute_total), (kd_risks, kd_total), brute_duration, kd_duration = compare_challenge_3_methods()

    print("Challenge 3 collision risks (brute force):", len(brute_risks))
    print(f"Challenge 3 total distance (brute force): {brute_total} m")
    print(f"Brute-force runtime: {brute_duration:.6f} s")
    print()
    print("Challenge 3 collision risks (k-d tree):", len(kd_risks))
    print(f"Challenge 3 total distance (k-d tree): {kd_total} m")
    print(f"k-d tree runtime: {kd_duration:.6f} s")

    if brute_risks != kd_risks or brute_total != kd_total:
        print()
        print("WARNING: brute-force and k-d tree results differ.")

    if kd_risks:
        print()
        print("Detected risks:")
        for risk in kd_risks:
            print(
                f"- {risk['satellite']} near {risk['debris']}: "
                f"{risk['distance_m']} m"
            )
