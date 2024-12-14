from fetch_advent_input import fetch_advent_input
import re
import time
import numpy as np
from sympy import symbols, Eq, solve, linsolve, S

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

example_input = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
example1_result = 480

def solve(input_string: str) -> int:
    cost_a = 3
    cost_b = 1
    result = 0
    #parse input
    machines = input_string.split("\n\n")
    for machine in machines:
        lines = machine.split("\n")
        button_a = lines[0].split(": ")[1]
        button_b = lines[1].split(": ")[1]
        prize = lines[2].split(": ")[1]
        button_a_x = int(re.search(r"X(\+|-)(\d+)", button_a).group(2))
        button_a_y = int(re.search(r"Y(\+|-)(\d+)", button_a).group(2))
        button_b_x = int(re.search(r"X(\+|-)(\d+)", button_b).group(2))
        button_b_y = int(re.search(r"Y(\+|-)(\d+)", button_b).group(2))
        prize_x = int(re.search(r"X=(\d+)", prize).group(1)) + 10000000000000
        prize_y = int(re.search(r"Y=(\d+)", prize).group(1)) + 10000000000000
        #calculate distances

        # Define variables
        x1, x2 = symbols('x1 x2', integer=True)  # Ensure variables are integers

        # Define equations
        eq1 = Eq(button_a_x * x1 + button_b_x * x2, prize_x)
        eq2 = Eq(button_a_y * x1 + button_b_y * x2, prize_y)

        # Solve the system for integer solutions
        solution = linsolve([eq1, eq2], (x1, x2))

        # Display the solutions
        print("Integer solutions:", solution)
        #check if solution is is integer 
        button_a = solution.args[0][0]
        button_b = solution.args[0][1]
        if button_a.is_integer and button_b.is_integer:
            result += button_a*cost_a + button_b*cost_b


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
problem_input = fetch_advent_input(13)

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