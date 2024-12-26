from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

example1_result = 3

def solve(input_string: str) -> int:
    # Parse input
    # Input is either lock or key
    # Lock starts with a line if #####
    # Key starts with a line of .....

    # Parse the input
    lock_list = []
    key_list = []
    result = 0
    lock_keys = input_string.split("\n\n")
    for lk in lock_keys:
        # create a list of lists
        lk_list = lk.split("\n")
        for i in range(len(lk_list)):
            lk_list[i] = list(lk_list[i])
        if lk.startswith("#####"):
            lock = True
        else:
            lock = False

        # Drop first and last line
        lk_list = lk_list[1:-1]
        if lock:
            # for the five collumns count number of # in each collumn
            collumn = []
            for i in range(5):
                count = 0
                for j in range(len(lk_list)):
                    if lk_list[j][i] == "#":
                        count += 1
                collumn.append(count)
            lock_list.append(collumn)
        else:
            # for the five collums count number of # in each collumn
            collumn = []
            for i in range(5):
                count = 0
                for j in range(len(lk_list)):
                    if lk_list[j][i] == "#":
                        count += 1
                collumn.append(count)
            key_list.append(collumn)
    
    result = 0
    # new check each key against each lock if sum of collumn is larger than 5 they will not match
    for lock in lock_list:
        for key in key_list:
            match = True
            for i in range(5):
                if lock[i] + key[i] > 5:
                    match = False
            if match:
                result += 1
    return result

# Test the example
result = solve(example_input)
if result == example1_result:
    print()
    print("The example result matches the expected result.")
    print()
else:
    print()
    print("The example result does not match the expected result. Got:", result, "Expected:", example1_result)
    print()

# Call the function and get the problem input
problem_input = fetch_advent_input(25)

if problem_input:
    problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    start_time = time.time()
    result = solve(problem_input)
    end_time = time.time()
    print()
    print("The result of this Part is:", result)
    print("Execution time was: ", end_time - start_time, "seconds.")
    print()