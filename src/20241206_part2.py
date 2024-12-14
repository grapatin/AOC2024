from fetch_advent_input import fetch_advent_input
import re

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
example1_result = 6

def move_and_check(input_dict, start_pos, direction):
    current_pos = start_pos
    #check if the next position is valid
    loop_true = False
    visited_positions = {}
    visited_positions_set = set()

    while True:
        next_pos = None
        if direction == "up":
            next_pos = (current_pos[0], current_pos[1] - 1)
        elif direction == "down":
            next_pos = (current_pos[0], current_pos[1] + 1)
        elif direction == "right":
            next_pos = (current_pos[0] + 1, current_pos[1])
        elif direction == "left":
            next_pos = (current_pos[0] - 1, current_pos[1])
        else:
            assert False, "Invalid direction"

        if next_pos in input_dict and input_dict[next_pos] == ".":
            #check if we are looping, i.e. we have been here before and direction is the same
            if str(next_pos)+input_dict[current_pos] in visited_positions_set:
                loop_true = True
                print("Loop detected")
                input_dict[current_pos] = "."
                input_dict[start_pos] = "^"
                break

            #remove "<" from current_pos
            current_char = input_dict[current_pos]

            input_dict[next_pos] = current_char
            visited_positions[next_pos] = current_char
            input_dict[current_pos] = "."
            visited_positions_set.add(str(next_pos)+current_char)
            #add "<" to next_pos
            current_pos = next_pos
        elif next_pos in input_dict and input_dict[next_pos] == "#":
            #direction turn 90 degrees to the right
            if direction == "up":
                direction = "right"
                #add ">" to current_pos
                input_dict[current_pos] = ">"
            elif direction == "right":
                direction = "down"
                #add "v" to current_pos
                input_dict[current_pos] = "v"
            elif direction == "down":
                direction = "left"
                #add "<" to current_pos
                input_dict[current_pos] = "<"
            elif direction == "left":
                direction = "up"
                #add "^" to current_pos
                input_dict[current_pos] = "^"
        elif next_pos not in input_dict:
            #we are going outside the map, ie we are done
            #clean up the last position
            input_dict[current_pos] = "."
            input_dict[start_pos] = "^"
            break
    return loop_true, visited_positions


def find_directions(input_dict, current_pos):
    current_char = input_dict[current_pos]
    if current_char == "^":
        return "up"
    elif current_char == "v":
        return "down"
    elif current_char == ">":
        return "right"
    elif current_char == "<":
        return "left"
    else:
        #assert False, "Invalid character"
        assert False, f"Invalid character: {current_char}"

def solve(input_string: str) -> int:
    visited_positions = {}
    input_dict = {}
    counter = 0
    #load input into dictionary with cords as key and value as the character
    for y, line in enumerate(input_string.split("\n")):
        for x, char in enumerate(line):
            input_dict[(x, y)] = char

    #find the starting position
    start_pos = [pos for pos, char in input_dict.items() if char == "^"][0]

    direction = find_directions(input_dict, start_pos)

    #first find current route for guard
    loop_true, visited_positions = move_and_check(input_dict, start_pos, direction)



    #add one # to the input_dict and check if we are looping
    for pos in visited_positions.keys():
        if pos == start_pos:
            continue
        if input_dict[pos] == ".":
            input_dict[pos] = "#"
            loop_true = False
            loop_true, visited_positions  = move_and_check(input_dict, start_pos, direction)
            input_dict[pos] = "."
            if loop_true:
                counter += 1


    return counter


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
problem_input = fetch_advent_input(6)

if problem_input:
    problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    result = solve(problem_input)
    print()
    print("The result of this Part is:", result)
    print()