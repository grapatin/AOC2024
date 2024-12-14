from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
example1_result = 36

#create recursive maze finder
#start position is input_pos, it is only allowed to move to the right, left, up or down
#allowed position are only those that increase value by 1
#find all paths that can be taken as counter
#return the number of paths that can be taken
def find_paths(input_pos, map_dict, path, values_found):   
    #check if the position is a valid position
    if input_pos in map_dict:
        value = map_dict[input_pos]
        #find all possible moves
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for move in moves:
            new_pos = (input_pos[0] + move[0], input_pos[1] + move[1])
            if new_pos in map_dict and map_dict[new_pos] == value + 1:
                #found a move
                path.append(new_pos)
                values_found.append(map_dict[new_pos])
                path, values_found = find_paths(new_pos, map_dict, path, values_found)
            
    return path, values_found

def solve(input_string: str) -> int:
    map_dict = {}
    #create a map of the input, x,y -> value
    for y, line in enumerate(input_string.split("\n")):
        for x, value in enumerate(line):
            map_dict[(x, y)] = int(value)

    paths = []
    values_found = []
    for pos in map_dict:
        if map_dict[pos] == 0:
            path, values_found_this_run = find_paths(pos, map_dict, [pos], [0])
            paths.append(path)
            values_found.append(values_found_this_run)
    
    #return number of 9s in the paths
    count = 0
    for path in paths:
        path_set = set()
        for pos in path:
            if map_dict[pos] == 9 and pos not in path_set:
                path_set.add(pos)
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
problem_input = fetch_advent_input(10)

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