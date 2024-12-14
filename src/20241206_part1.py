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
example1_result = 41

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
    visited_positions = set()
    input_dict = {}
    #load input into dictionary with cords as key and value as the character
    for y, line in enumerate(input_string.split("\n")):
        for x, char in enumerate(line):
            input_dict[(x, y)] = char

    #find the starting position
    start_pos = [pos for pos, char in input_dict.items() if char == "^"][0]
    visited_positions.add(start_pos)
    current_pos = start_pos
    direction = find_directions(input_dict, current_pos)
    #check if the next position is valid
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
            visited_positions.add(next_pos)
            #remove "<" from current_pos
            input_dict[current_pos] = "."
            #add "<" to next_pos
            input_dict[next_pos] = "^"
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
            break

    return len(visited_positions)


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