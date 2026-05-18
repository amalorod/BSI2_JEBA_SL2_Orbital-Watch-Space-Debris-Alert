


from src.challenge1 import run_challenge_1
from src.challenge2 import run_challenge_2
from src.challenge3 import run_challenge_3
from src.challenge3 import compare_challenge_3_methods



def main():
    print("Orbital Watch – Space Debris Alert")
    print("----------------------------------")

    result_one = run_challenge_1()
    print(f"Challenge 1 result: {result_one}")

    result_two = run_challenge_2()
    print(f"Challenge 2 result: {result_two}")

    (brute_risks, brute_total), (kd_risks, kd_total), brute_time, kd_time = compare_challenge_3_methods()
    print()
    print("Challenge 3 (Brute Force):")
    print(f"Collision risks: {len(brute_risks)}")
    print(f"Total distance: {brute_total} m")
    print(f"Runtime: {brute_time:.6f} s")

    print()
    print("Challenge 3 (KD-Tree):")
    print(f"Collision risks: {len(kd_risks)}")
    print(f"Total distance: {kd_total} m")
    print(f"Runtime: {kd_time:.6f} s")


    
    print()
    print("Detected risks:")

    for risk in kd_risks:
        print(
            f"- {risk['satellite']} near {risk['debris']}: "
            f"{risk['distance_m']} m"
        )



if __name__ == "__main__":
    main()