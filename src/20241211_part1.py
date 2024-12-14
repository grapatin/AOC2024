from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """125 17"""
example1_result = 55312

def solve(input_string: str) -> int:
    #parse the input into a list of integers
    input_list = list(map(int, input_string.split()))
    #these are the rules for the problem
    #if 0 change 1
    #if even number of digits split into 2 left and right
    #if none applie multiply with 2024 
    #do 25 looops
    #return how long the list is
    for i in range(25):
        new_list = []
        for number in input_list:
            if number == 0:
                new_list.append(1)
            elif len(str(number)) % 2 == 0:
                left = str(number)[:len(str(number))//2]
                right = str(number)[len(str(number))//2:]
                #insert left and right into new_list at same place as number
                new_list.append(int(left))
                new_list.append(int(right))
            else:
                new_list.append(number*2024)
        input_list = new_list
        #print(input_list, '\n')
        

    return len(input_list)

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
problem_input = fetch_advent_input(11)

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