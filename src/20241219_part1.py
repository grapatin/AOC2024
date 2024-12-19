from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
example1_result = 6

def solve(input_string: str) -> int:
    possible_colors_list, desired_combinations = input_string.split("\n\n")

    possible_colors_list = possible_colors_list.split(", ")
    possible_colors_dict = {}
    min_length = 10000000
    max_length = 0
    for i, color in enumerate(possible_colors_list):
        possible_colors_dict[color] = i
        min_length = min(min_length, len(color))
        max_length = max(max_length, len(color))

    desired_combinations = desired_combinations.split("\n")
    result = 0

    for desired_combination in desired_combinations:
        remove_duplicates = set()
        queue = []
        for l in range(min_length, max_length + 1):
            # append all possible length combination but check so we are not out of bounds
            if len(desired_combination) >= l:
                queue.append(((desired_combination[:l]), desired_combination[l:]))

        while queue:
            current, whats_is_remaining = queue.pop(0)
            if current in possible_colors_dict:
                # Found a match
                if whats_is_remaining:
                    if whats_is_remaining not in remove_duplicates:
                        remove_duplicates.add(whats_is_remaining)
                        for l in range(min_length, max_length + 1):
                            if len(desired_combination) >= l:
                                queue.append((whats_is_remaining[:l], whats_is_remaining[l:]))
                else:
                    #  Found a complete match                  
                    result += 1
                    break

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
problem_input = fetch_advent_input(19)

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