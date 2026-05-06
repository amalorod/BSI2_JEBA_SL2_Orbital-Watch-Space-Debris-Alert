


from src.challenge1 import run_challenge_1
from src.challenge2 import run_challenge_2
from src.challenge3 import run_challenge_3



def main():
    print("Orbital Watch – Space Debris Alert")
    print("----------------------------------")

    result_one = run_challenge_1()
    print(f"Challenge 1 result: {result_one}")

    result_two = run_challenge_2()
    print(f"Challenge 2 result: {result_two}")

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


if __name__ == "__main__":
    main()