from fetch_advent_input import fetch_advent_input
import re

example_input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
example1_result = 2

def solve(input_string: str) -> int:
    count = 0
    #go through each line and get an array of numbers
    for line in input_string.split('\n'):
        if line:
            linegood = True
            numbers = list(map(int, re.findall(r'\d+', line)))
            #go through the list and check if the increase by at least 1 and at most 3
            #if they do, increment the count
            direction = 0
            for i in range(1, len(numbers)):
                if abs(numbers[i] - numbers[i-1]) >= 1 and abs(numbers[i] - numbers[i-1]) <= 3:
                    pass
                else:
                    linegood = False
                    break
            #check direction
            if linegood:
                for i in range(1, len(numbers)):
                    if numbers[i] - numbers[i-1] > 0:
                        if direction == 0:
                            direction = 1
                        elif direction == -1:
                            linegood = False
                            break
                    elif numbers[i] - numbers[i-1] < 0:
                        if direction == 0:
                            direction = -1
                        elif direction == 1:
                            linegood = False
            if linegood:
                count += 1
    return count

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
problem_input = fetch_advent_input(2)
if problem_input:
    # Use the problem_input variable as needed
    result = solve(problem_input)
    print()
    print("The result is Part 1:", result)
    print()