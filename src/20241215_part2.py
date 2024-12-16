from fetch_advent_input import fetch_advent_input
import re
import time
import copy

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

example1_result = 10092

def pretty_print_map(map_dict):
    # Get the max x and y values
    max_x = max(map_dict.keys(), key=lambda x: x[0])[0]
    max_y = max(map_dict.keys(), key=lambda x: x[1])[1]

    # Loop through the map and print it
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(map_dict.get((x, y), " "), end="")
        print()

def check_next_pos(map_dict, next_pos, directioncord):
    # Only look for the next pos and if it is a box, then return the 2 cords for the found box
    # if it is a wall, return false
    # if it is a empty space return true
    # if it is a box, return the 2 cords for the found box

    # Check if the new position is a wall
    if map_dict.get(next_pos) == "#":
        return "wall", (0,0), (0,0)
    elif map_dict.get(next_pos) == ".":
        return "empty", (0,0), (0,0)
    elif map_dict.get(next_pos) == "[":
        # box found, return cords for the box
        box_cords_left_side = next_pos
        box_cords_right_side = (next_pos[0] + 1, next_pos[1])
        return "box", box_cords_left_side, box_cords_right_side
    elif map_dict.get(next_pos) == "]":
        # box found, return cords for the box
        box_cords_left_side = (next_pos[0] - 1, next_pos[1])
        box_cords_right_side = next_pos
        return "box", box_cords_left_side, box_cords_right_side
    else:      
        # Unexpected character, do an assert
        assert False

def solve(input_string: str) -> int:
    # Split the input into the map and the directions
    map_str, directions = input_string.split("\n\n")
    map_str = map_str.strip()

    # directions can also contain newlines, so we need to remove them
    directions = directions.replace("\n", "")

    # Create a map_dict to store the map
    map_dict = {}
    x = 0
    y = 0
    for char in map_str:
        if char == "\n":
            y += 1
            x = 0
        else:
            if char == "@":
                char = "@."
            elif char == "O":
                char = "[]"
            elif char == "#":
                char = "##"
            elif char == ".":
                char = ".."
            map_dict[(x, y)] = char[0]
            x += 1
            map_dict[(x, y)] = char[1]
            x += 1

    # Now move robot '@' around the map
    # '#' is a wall
    # '.' is an empty space
    # '[]' is a box
    # Boxes can be pushed but not into wall, if multiple boxes are pushed, they will move in the same direction
    # We need make sure the full box moves in the same direction and keep together
    # And one box could push 2 other boxes depending on how they lign up
    # '^' is up, 'v' is down, '<' is left, '>' is right
    # robot move according to the directions given in the input

    # First find the starting position of the robot
    robot_pos = None
    for pos, char in map_dict.items():
        if char == "@":
            robot_pos = pos
            break
    directioncord = (0, 0)

    print("Initial state")
    pretty_print_map(map_dict)

    for char in directions:
        # Move the robot
        if char == "^":
            new_pos = (robot_pos[0], robot_pos[1] - 1)
            directioncord = (0, -1)
        elif char == "v":
            new_pos = (robot_pos[0], robot_pos[1] + 1)
            directioncord = (0, 1)
        elif char == "<":
            new_pos = (robot_pos[0] - 1, robot_pos[1])
            directioncord = (-1, 0)
        elif char == ">":
            new_pos = (robot_pos[0] + 1, robot_pos[1])
            directioncord = (1, 0)
        #print("Move", char)
        # Check if the new position is a wall
        if map_dict.get(new_pos) == "#":
            # we cannot move
            continue
        # Check if the new position is a box
        elif map_dict.get(new_pos) in "[]":
            # we have a box, we need to check to see if both sides of the box can be moved
            # list of cords with boxes
            existing_box_cords = set()
            coords_to_check = set()
            existing_box_cords.add(new_pos)
            coords_to_check.add(new_pos)
            if map_dict.get(new_pos) == "[":
                existing_box_cords.add((new_pos[0] + 1, new_pos[1]))
                coords_to_check.add((new_pos[0] + 1, new_pos[1]))
            else:
                existing_box_cords.add((new_pos[0] - 1, new_pos[1]))
                coords_to_check.add((new_pos[0] - 1, new_pos[1]))

            move_possible = True
            while coords_to_check:
                # check the next box
                next_box = coords_to_check.pop()
                next_pos = (next_box[0] + directioncord[0], next_box[1] + directioncord[1])
                result_type, box_cords_left_side, box_cords_right_side = check_next_pos(map_dict, next_pos, directioncord)
                if result_type == "wall":
                    move_possible = False
                    coords_to_check = []
                    break
                elif result_type == "empty":
                    # Empty space, we can move the box
                    pass
                elif result_type == "box":
                    # Another box, we need to move it as well but make sure we have not already checked this box
                    if box_cords_left_side not in existing_box_cords:
                        existing_box_cords.add(box_cords_left_side)
                        coords_to_check.add(box_cords_left_side)
                    if box_cords_right_side not in existing_box_cords:
                        existing_box_cords.add(box_cords_right_side)
                        coords_to_check.add(box_cords_right_side)
                else:
                    # Unexpected character, do an assert
                    assert False

            if not move_possible:
                continue
            else:
                # Move the boxes and robot
                # create a working deep copy of the map_dict
                space_left = set()
                spaces_occupied = set()

                new_map_dict = map_dict.copy()
                for box in existing_box_cords:
                    new_box_pos = (box[0] + directioncord[0], box[1] + directioncord[1])
                    new_map_dict[new_box_pos] = map_dict.get(box)
                    space_left.add(box)
                    spaces_occupied.add(new_box_pos) 
                
                for occupied in spaces_occupied:
                    space_left.discard(occupied)

                for space in space_left:
                    new_map_dict[space] = "."

                new_map_dict[robot_pos] = "."
                new_map_dict[new_pos] = "@"
                robot_pos = new_pos
                map_dict = new_map_dict
        # Check if the new position is an empty space
        elif map_dict.get(new_pos) in " .":
            map_dict[robot_pos] = "."
            map_dict[new_pos] = "@"
            robot_pos = new_pos

    pretty_print_map(map_dict)
    result = 0
    for pos, char in map_dict.items():
        if char == "[":
            result += pos[0] + pos[1]*100

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
problem_input = fetch_advent_input(15)

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