from fetch_advent_input import fetch_advent_input
import re

# Define a debug flag
DEBUG = True

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """2333133121414131402"""
example1_result = 2858

#create a structure to hold the file_id and size
class file:
    def __init__(self, file_id, size, empty):
        self.file_id = file_id
        self.size = size
        self.empty = empty
        self.moved = False

def solve(input_string: str) -> int:
    file_disk_list = []
    file_number = 0
    while input_string:
        number = input_string[0]
        input_string = input_string[1:]
        file_obj = file(file_number, int(number), False)
        file_number += 1
        file_disk_list.append(file_obj)
        if len(input_string) != 0:            
            len_of_empty = input_string[0]
            input_string = input_string[1:]
            file_obj = file(0, int(len_of_empty), True)
            file_disk_list.append(file_obj)
 
    #now condense the filesystem
    done = False
    #search from backwards
    # find the last non empty file
    # and insert it into the first empty spot large enough to fill the hole file
    # make sure to update the empty size of the blocked filled by the new file alse make sure that the order is fixed
    # only go through the list once

    for i in range(len(file_disk_list) - 1, 0, -1):
        last_file = file_disk_list[i]
        #check if the file is empty
        if last_file.empty != True and last_file.moved != True:
            #now try to find first place that can fit the file that is ahead of this file space
            size = last_file.size
            last_file.moved = True
            for j in range(0, i):
                if file_disk_list[j].empty == True and file_disk_list[j].size >= size:
                    #found a spot
                    empty_spot = file_disk_list[j]
                    #copy the file to the empty spot
                    new_copy = file(last_file.file_id, size, False)
                    file_disk_list[j] = new_copy
                    #update the empty spot
                    empty_spot.size -= size
                    #insert the empty spot right after the file in the list
                    file_disk_list.insert(j + 1, empty_spot)
                    #mark the moved file as empty file now
                    last_file.empty = True
                    #printer(file_disk_list)
                    break


    #calculate checksum
    printer(file_disk_list)
    checksum = 0
    counter = 0
    for i in range(0, len(file_disk_list)):
        size = file_disk_list[i].size
        file_id = file_disk_list[i].file_id
        empty = file_disk_list[i].empty
        for j in range(0, size):
            if empty:
                pass
            else:
                checksum += file_id*counter
            counter += 1

    return checksum

def printer(file_disk_list):
    file_string = ''
    for i in range(0, len(file_disk_list)):
        size = file_disk_list[i].size
        file_id = file_disk_list[i].file_id
        empty = file_disk_list[i].empty
        for j in range(0, size):
            if empty:
                file_string += '.'
            else:
                file_string += str('*')

    debug_print(file_string)


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