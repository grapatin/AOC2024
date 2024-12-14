from fetch_advent_input import fetch_advent_input
import re

example_input = """3   4
4   3
2   5
1   3
3   9
3   3"""
example1_result = 11

def solve(input_string: str) -> int:
    # go through each line of the input
    # split the line into two numbers
    # store first number in a sorted list
    # store second number in a sorted list
    # sum the difference between the first and last number in the list
    # return the sum
    sum = 0
    number1 = []
    number2 = []
    for line in input_string.split('\n'):
        if line:
            numbers = list(map(int, re.findall(r'\d+', line)))
            #add to list number1 and number2
            number1.append(numbers[0])
            number2.append(numbers[1])

    #sort the lists
    # get the difference between the first and last number in the list
    # add the difference to the sum
    # return the sum

    number1.sort()
    number2.sort()
    #for each number in the list, get the difference between the first and last number
    for i in range(len(number1)):
        sum += abs(number1[i] - number2[i])
        
    return sum

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
problem_input = fetch_advent_input(1)
if problem_input:
    # Use the problem_input variable as needed
    result = solve(problem_input)
    print()
    print("The result is Part 1:", result)
    print()