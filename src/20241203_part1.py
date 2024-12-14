from fetch_advent_input import fetch_advent_input
import re

example_input = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
example1_result = 161

def solve(input_string: str) -> int:
    #find exact matches of mul(x,y) where x and y are numbers 3 digits or less
    #add x*y to the total
    #find the next mul and repeat
    total = 0
    while True:
        match = re.search(r'mul\((\d{1,3}),(\d{1,3})\)', input_string)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            total += x * y
            input_string = input_string[match.end():]
        else:
            break

    return total


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
problem_input = fetch_advent_input(3)
if problem_input:
    #trim input
    #problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    result = solve(problem_input)
    print()
    print("The result of this Part is:", result)
    print()