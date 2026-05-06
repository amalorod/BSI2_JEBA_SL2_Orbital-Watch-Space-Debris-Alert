from src.challenges import challenge_one, challenge_two, challenge_three


def main():
    print("Orbital Watch – Space Debris Alert")
    print("----------------------------------")

    result_one = challenge_one()
    print(f"Challenge 1 result: {result_one}")

    result_two = challenge_two()
    print(f"Challenge 2 result: {result_two}")

    risks, total_distance_m = challenge_three()
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


if __name__ == "__main__":
    main()