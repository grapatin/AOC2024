from fetch_advent_input import fetch_advent_input
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
example1_result = 34

def solve(input_string: str) -> int:
    map_dict = {}
    output_dict = {}
    lines = input_string.split("\n")
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            #store the coordinates in the dict
            map_dict[(x, y)] = char
            output_dict[(x, y)] = char
    for key in map_dict:
        if map_dict[key] != ".":
            antenna_type = map_dict[key]
            x, y = key
            for key2 in map_dict:
                if map_dict[key2] == antenna_type:
                    x2, y2 = key2
                    if x2 != x or y2 != y:
                        delta_x = x2 - x
                        delta_y = y2 - y
                        for i in range(1, 100):
                            possible_antinode_cord = (x + delta_x*i, y + delta_y*i)
                            if possible_antinode_cord in map_dict:
                                output_dict[possible_antinode_cord] = "#"
                            else:
                                break
                        if possible_antinode_cord in map_dict:
                            output_dict[possible_antinode_cord] = "#"
    print_map(output_dict)
    number_of_anti_nodes = sum([1 for key in output_dict if output_dict[key] == "#"])
    return number_of_anti_nodes
                        
def print_map(map_dict):
    if DEBUG:
        #get the max x and y coordinates
        max_x = max(map_dict, key=lambda x: x[0])[0]
        max_y = max(map_dict, key=lambda x: x[1])[1]
        #iterate over the map and print the map
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                print(map_dict[(x, y)], end="")
            print()

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
problem_input = fetch_advent_input(8)

if problem_input:
    problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    start_time = time.time()
    result = solve(problem_input)
    end_time = time.time()
    print()
    print("The result of this Part is:", result)
    print("Time taken:", end_time - start_time, "seconds.")
    print()