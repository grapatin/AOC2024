from fetch_advent_input import fetch_advent_input
import re

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
example1_result = 14

def solve(input_string: str) -> int:
    #create a dict to store the coordinates of the map
    map_dict = {}
    output_dict = {}
    #split the input string into lines
    lines = input_string.split("\n")
    #iterate over the lines to get the coordinates
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            #store the coordinates in the dict
            map_dict[(x, y)] = char
            output_dict[(x, y)] = char

    #Go through the map and for each antenna (not a .) check the distance to all the other antennas of same type
    #only look forward in the map to avoid double counting
    #if the found antinode is within the map count it
    number_of_anti_nodes = 0
    for key in map_dict:
        if map_dict[key] != ".":
            #get the type of the antenna
            antenna_type = map_dict[key]
            #get the coordinates of the antenna
            antenna_coords = key
            #get the x and y coordinates
            x, y = key
            #iterate over the map to find the other antennas of the same type ignore same antenna
            for key2 in map_dict:
                if map_dict[key2] == antenna_type:
                    #check if antenna is forward in the map
                    x2, y2 = key2
                    if x2 != x or y2 != y:
                        delta_x = x2 - x
                        delta_y = y2 - y
                        possible_antinode_cord = (x + delta_x*-1, y + delta_y*-1)
                        #check if the possible antinode is within the map
                        if possible_antinode_cord in map_dict:
                            number_of_anti_nodes += 1
                            output_dict[possible_antinode_cord] = "#"
    print_map(output_dict)
    #count number of # in the output dict
    number_of_anti_nodes = sum([1 for key in output_dict if output_dict[key] == "#"])
    

    return number_of_anti_nodes
                        
def print_map(map_dict):
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
    result = solve(problem_input)
    print()
    print("The result of this Part is:", result)
    print()