from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
example1_result = 1930

def pretty_print_map(map_dict):
    #get the max x and y values
    max_x = max([x for x,y in map_dict.keys()])
    max_y = max([y for x,y in map_dict.keys()])
    #print the map
    for y in range(max_y+1):
        for x in range(max_x+1):
            if (x,y) not in map_dict:
                print(" ", end="")
            else:
                print(map_dict[(x,y)], end="")
        print()
    


def solve(input_string: str) -> int:
    #create a map dict of the input, x,y -> value
    map_dict = {}
    search_area_dict = {}
    for y, line in enumerate(input_string.split("\n")):
        for x, value in enumerate(line):
            map_dict[(x,y)] = value
            search_area_dict[(x,y)] = value
    
    #find each group of each letter in map_dict that is connected
    #create a new map_dict for each found group
    #save all new map_dicts in a list
    groups_of_crop = []

    while search_area_dict:
        #pop first position in search_area_dict
        current_position = search_area_dict.popitem()[0]
        #create a new map_dict for this group
        new_crop_map_dict = {}
        current_crop = map_dict[current_position]

        #create a list of positions to check
        positions_to_check = [current_position]
        while positions_to_check:
            #get the first position in the list but leave it in dict
            position = positions_to_check.pop(0)
            #if the position is not in the new_map_dict, add it
            if position not in new_crop_map_dict and position in map_dict and map_dict[position] == current_crop:
                new_crop_map_dict[position] = map_dict[position]
                if position in search_area_dict:
                    search_area_dict.pop(position)
                #add the positions around this position to the list
                x,y = position
                positions_to_check.extend([(x+1,y), (x-1,y), (x,y+1), (x,y-1)])
        #add the new_map_dict to the groups list
        groups_of_crop.append(new_crop_map_dict)
        #find the next position in the map_dict
        current_position = None

    #print all crops
    for crop in groups_of_crop:
        pretty_print_map(crop)
        print("size of crop:", len(crop))
        print()

    result = 0
    for crop in groups_of_crop:
        #lets find out curcovention of the crop
        #find the top left corner of the crop
        #for each position in the crop, check how many positions that are outside the crop
        outside_dict = dict()
        crop_type = None
        for position in crop:
            x,y = position
            crop_type = crop[position]
            for x1,y1 in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]:
                if (x1,y1) not in crop:
                    #create strings from x and y and x1 and y1
                    x_str = str(x)
                    y_str = str(y)
                    x1_str = str(x1)
                    y1_str = str(y1)
                    #add the outside position to the outside_dict
                    outside_dict[x1_str+y1_str + x_str + y_str] = crop_type                    
        outside_count = len(outside_dict)
        sie_of_crop = len(crop)
        result += sie_of_crop*outside_count
        print("crop_type:", crop_type, "size of crop:", sie_of_crop, "outside_count:", outside_count, "result:", sie_of_crop*outside_count)
    return result

        

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
problem_input = fetch_advent_input(12)

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