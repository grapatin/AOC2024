from fetch_advent_input import fetch_advent_input
import re
import time

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
        prize_x = int(re.search(r"X=(\d+)", prize).group(1))
        prize_y = int(re.search(r"Y=(\d+)", prize).group(1))

        ##create a goal list of cords with prize - button_b*n
        goal_list = []
        n = 1
        button_b_pressed = 0
        button_a_pressed = 0

        while True:
            goal_list.append((prize_x - button_b_x*n, prize_y - button_b_y*n))
            n += 1
            if n > 100:
                break

        n = 1
        success = False
        pos = (0,0)
        while True:
            if pos in goal_list:
                break
            else:
                pos = (pos[0] + button_a_x, pos[1] + button_a_y)
                if pos in goal_list:
                    success = True
                    button_a_pressed = n
                    break
                elif n > 100:
                    break
            n += 1
        #calculate cost
        if success:
            button_b_pressed = goal_list.index(pos) + 1
            result += button_a_pressed*cost_a + button_b_pressed*cost_b

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