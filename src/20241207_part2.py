from fetch_advent_input import fetch_advent_input
from typing import List
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""


example1_result = 11387

def math_operation_recursive(a :int, b : List[int], calibration_result) -> int:
    for operator in ["+", "*", "||"]:
        if operator == "+":
            result = a + b[0]
            c = b[1:]
            if not c:
                if result == calibration_result:
                    return result
            else:
                if calibration_result == math_operation_recursive(result, c, calibration_result):
                    return calibration_result
        elif operator == "*":
            result = a * b[0]
            c = b[1:]
            if not c:
                if result == calibration_result:
                    return result
            else:
                if calibration_result == math_operation_recursive(result, c, calibration_result):
                    return calibration_result
        elif operator == "||":
            result = int(str(a) + str(b[0]))
            c = b[1:]
            if not c:
                if result == calibration_result:
                    return result
            else:
                if calibration_result == math_operation_recursive(result, c, calibration_result):
                    return calibration_result
    return 0

def solve(input_string: str) -> int:
    solution = 0
    #go through each line of the input
    for line in input_string.split("\n"):
        #split the line into the depth and the range
        calibration_result, input_int = line.split(": ")
        calibration_result = int(calibration_result)
        test_values = list(map(int, input_int.split(" ")))

        #by either using + or * on each test_value, can we get the test_value
        #if so add test_value to result
        #we have 2 different possible operator try both
        temp_result = test_values[0]
        test_values = test_values[1:]
        result = math_operation_recursive(temp_result, test_values, calibration_result)
        if result == calibration_result:
            solution += result

    return solution

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
problem_input = fetch_advent_input(7)

if problem_input:
    problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    start_time = time.time()
    result = solve(problem_input)
    end_time = time.time()
    print()
    print("The result of this Part is:", result)
    print("execution time:", end_time - start_time, "seconds.")
    print()