from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

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
            map_dict[(x, y)] = char
            x += 1

    # Now move robot '@' around the map
    # '#' is a wall
    # '.' is an empty space
    # 'O' is a box
    # Boxes can be pushed but not into wall, if multiple boxes are pushed, they will move in the same direction
    # '^' is up, 'v' is down, '<' is left, '>' is right
    # robot move according to the directions given in the input

    # First find the starting position of the robot
    robot_pos = None
    for pos, char in map_dict.items():
        if char == "@":
            robot_pos = pos
            break
    directioncord = (0, 0)

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

        # Check if the new position is a wall
        if map_dict.get(new_pos) == "#":
            continue

        # Check if the new position is a box
        if map_dict.get(new_pos) == "O":
            numberOfBoxes = 1
            move_possible = True
            # Check if the box can be pushed and make sure to handle scenarios where multiple boxes are pushed
            # Search until a '.' or a '#' is found
            while True:
                next_pos = (new_pos[0] + directioncord[0] * numberOfBoxes, new_pos[1] + directioncord[1] * numberOfBoxes)
                if map_dict.get(next_pos) == "#":
                    move_possible = False
                    break
                elif map_dict.get(next_pos) in " .":
                    # Empty space or a target, we can move the box
                    break
                elif map_dict.get(next_pos) == "O":
                    # Another box, we need to move it as well
                    numberOfBoxes += 1
                else:
                    # Unexpected character, do an assert
                    assert False
                    
            if not move_possible:
                continue
            else:
                new_box_pos = (new_pos[0] + directioncord[0]*numberOfBoxes, new_pos[1] + directioncord[1]*numberOfBoxes)
                #move the first box to the new position
                map_dict[new_pos] = "."
                map_dict[new_box_pos] = "O"

        map_dict[robot_pos] = " "
        map_dict[new_pos] = "@"
        robot_pos = new_pos

    pretty_print_map(map_dict)
    result = 0
    for pos, char in map_dict.items():
        if char == "O":
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