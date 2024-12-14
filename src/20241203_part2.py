from fetch_advent_input import fetch_advent_input
import re

example_input = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
example1_result = 48

def solve(input_string: str) -> int:
    total = 0
    do_active = True
    while True:
        # find exact matches of mul(x,y) where x and y are numbers 3 digits or less
        # but also find all don't() and do()
        match = re.search(r"(mul\((\d{1,3}),(\d{1,3})\))|(do\(\))|(don't\(\))", input_string)
        if match:
            if match.group(1):  # mul(x,y) match
                x = int(match.group(2))
                y = int(match.group(3))
                if do_active:
                    total += x * y
            elif match.group(4):  # do() match
                do_active = True
            elif match.group(5):  # don't() match
                do_active = False
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