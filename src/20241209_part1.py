from fetch_advent_input import fetch_advent_input
import re

# Define a debug flag
DEBUG = True

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """2333133121414131402"""
example1_result = 1928

def solve(input_string: str) -> int:
    file_disk_list = []
    done = False
    file_number = 0
    while not done:
        number = input_string[0]
        input_string = input_string[1:]
        for i in range(0, int(number)):
            file_disk_list.append(file_number)
        if len(input_string) != 0:            
            file_number += 1
            empty = input_string[0]
            input_string = input_string[1:]
            for i in range(0, int(empty)):
                file_disk_list.append('.')
        if len(input_string) == 0:
            done = True 

    #create one long string for list
    file_string = ''.join(map(str, file_disk_list))
    debug_print(file_string)

    #take the last file and insert into first empty spot and do so until no more empty spots
    done = False
    while not done:
        adjusted_length = len(file_disk_list)
        for i in range(0, len(file_disk_list)):
            done = True
            if file_disk_list[i] == '.' and i < adjusted_length:
                #find last non empy disk
                #search backwards
                for j in range(len(file_disk_list) - 1, 0, -1):
                    if file_disk_list[j] != '.': 
                        file_disk_list[i] = file_disk_list[j]
                        file_disk_list[j] = '.'               
                        done = False
                        adjusted_length -= 1
                        break
    file_string = ''.join(map(str, file_disk_list))   
    debug_print(file_string)
    #calculate checksum
    checksum = 0
    counter = 0
    for i in range(0, len(file_disk_list)):
        if file_disk_list[i] != '.':
            checksum += file_disk_list[i]*counter
            counter += 1
    return checksum

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
problem_input = fetch_advent_input(9)

if problem_input:
    problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    result = solve(problem_input)
    print()
    print("The result of this Part is:", result)
    print()