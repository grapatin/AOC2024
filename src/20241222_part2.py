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
2
3
2024"""

#example_input = "123"
example1_result = 23

def solve(input_string: str) -> int:
    result = 0
    list_of_lists = []
    dict_prices_of = {}

    for monkey, line in enumerate(input_string.split("\n")):
        starting_number = int(line)

        number_of_loops = 2000

        secret_number = starting_number
        secret_list = []  
        #create a list that contain the last 4 numbers in loop
        last_4 = []
        #only store the first occurence of the key
        key_set = set()

        for i in range(number_of_loops):
            before = secret_number
            m_64 = secret_number * 64
            secret_number = secret_number ^ m_64
            secret_number = secret_number % 16777216

            d_32 = secret_number // 32
            secret_number = secret_number ^ d_32
            secret_number = secret_number % 16777216

            m_2048 = secret_number * 2048
            secret_number = m_2048 ^ secret_number
            secret_number = secret_number % 16777216

            secret_list.append(secret_number)
            delta = (secret_number % 10) - (before % 10)
            last_4.append(delta)
            if i > 3:
                last_4.pop(0)
                key = tuple(last_4)
                if key == (-2,1,-1,3):
                    print("Found the key at", i, "for starting number", starting_number, "cost is ", secret_number % 10)    
                if key in dict_prices_of and key not in key_set:
                    key_set.add(key)
                    dict_prices_of[key] += secret_number % 10
                elif key not in dict_prices_of:
                    key_set.add(key)
                    dict_prices_of[key] = secret_number % 10
                
        list_of_lists.append(secret_list)
            
    # dict_prices find the highest value
    highest_value = 0
    highest_key = None
    for key, value in dict_prices_of.items():
        if value > highest_value:
            highest_value = value
            highest_key = key

    return highest_value

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