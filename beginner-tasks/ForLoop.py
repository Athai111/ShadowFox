# 1. Dice Simulation
import random

rolls = 20
count_6 = 0
count_1 = 0
two_6_in_row = 0

prev_roll = None

for i in range(rolls):
    roll = random.randint(1, 6)
    print(f"Roll {i+1}: {roll}")

    if roll == 6:
        count_6 += 1
    if roll == 1:
        count_1 += 1

    if roll == 6 and prev_roll == 6:
        two_6_in_row += 1

    prev_roll = roll

print("\n--- Statistics ---")
print("Number of times rolled 6:", count_6)
print("Number of times rolled 1:", count_1)
print("Number of times two 6s in a row:", two_6_in_row)
'''
Key Logic:
random.randint(1,6) → simulates dice
prev_roll → tracks previous value
Condition:
if roll == 6 and prev_roll == 6
→ counts consecutive 6s
'''

# 2. Jumping Jacks Workout Program
total_jacks = 100
done = 0

for i in range(10, total_jacks + 1, 10):
    print(f"\nPerform {10} jumping jacks")
    done += 10

    tired = input("Are you tired? (yes/y or no/n): ").lower()

    if tired == "yes" or tired == "y":
        skip = input("Do you want to skip the remaining sets? (yes/y or no/n): ").lower()
        
        if skip == "yes" or skip == "y":
            print(f"You completed a total of {done} jumping jacks.")
            break
    else:
        remaining = total_jacks - done
        print(f"{remaining} jumping jacks remaining.")

# If loop completes fully
if done == total_jacks:
    print("Congratulations! You completed the workout.")
'''
Logic Breakdown:
Loop runs in steps of 10 → range(10, 101, 10)
done tracks total completed
Takes user input
Uses:
break → exit early
condition check → continue or stop
'''
