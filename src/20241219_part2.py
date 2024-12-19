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
example1_result = 16

def cache(func):
    memo = {}
    def wrapper(*args):
        if args not in memo:
            memo[args] = func(*args)
        return memo[args]
    return wrapper

@cache
def recursive_search(current, what_is_remaining, min_length, max_length):
    count = 0
    if current in possible_colors_dict:
        # Found a match
        if what_is_remaining:
            for l in range(min_length, max_length + 1):
                if len(what_is_remaining) >= l:
                    count += recursive_search(what_is_remaining[:l], what_is_remaining[l:], min_length, max_length)
        else:
            #  Found a complete match
            return 1
    return count

possible_colors_dict = {}

def solve(input_string: str) -> int:
    possible_colors_list, desired_combinations = input_string.split("\n\n")

    possible_colors_list = possible_colors_list.split(", ")
    
    min_length = 10000000
    max_length = 0
    for i, color in enumerate(possible_colors_list):
        possible_colors_dict[color] = i
        min_length = min(min_length, len(color))
        max_length = max(max_length, len(color))

    desired_combinations = desired_combinations.split("\n")
    result = 0

    for desired_combination in desired_combinations:
        for l in range(min_length, max_length + 1):
            # append all possible length combination but check so we are not out of bounds
            if len(desired_combination) >= l:
                result += recursive_search(desired_combination[:l], desired_combination[l:], min_length, max_length)
        print('A result found', result)

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
    possible_colors_dict = {}
    problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    start_time = time.time()
    result = solve(problem_input)
    end_time = time.time()
    print()
    print("The result of this Part is:", result)
    print("Execution time was: ", end_time - start_time, "seconds.")
    print()