from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """1
10
100
2024"""


example1_result = 37327623

def solve(input_string: str) -> int:
    result = 0

    for line in input_string.split("\n"):
        starting_number = int(line)

        number_of_loops = 2000

        secret_number = starting_number
        for i in range(number_of_loops):
            m_64 = secret_number * 64
            secret_number = secret_number ^ m_64
            secret_number = secret_number % 16777216

            d_32 = secret_number // 32
            secret_number = secret_number ^ d_32
            secret_number = secret_number % 16777216

            m_2048 = secret_number * 2048
            secret_number = m_2048 ^ secret_number
            secret_number = secret_number % 16777216

        result += secret_number

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
problem_input = fetch_advent_input(22)

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