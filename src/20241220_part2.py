from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
example1_result = 285

def solve(input_string: str, limit) -> int:
    # Create a map dict with x, y as key and the value as the character
    map_dict = {}
    start_pos = None
    end_pos = None
    for y, line in enumerate(input_string.split("\n")):
        for x, char in enumerate(line):
            map_dict[(x, y)] = char
            if char == "S":
                start_pos = (x, y)
            if char == "E":
                end_pos = (x, y)

    # Solve the maze with BFS
    queue = []
    queue.append((start_pos, 0))
    visited = dict()
    visited[start_pos] = 0
    visited_list = []
    visited_list.append(start_pos)

    while queue:
        current_pos, current_steps = queue.pop(0)
        x, y = current_pos

        if current_pos == end_pos:
            # We have reached the end
            print("Reached the end in", current_steps, "steps")
            continue

        # Check the neighbors
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x = x + dx
            new_y = y + dy
            new_pos = (new_x, new_y)

            if new_pos in visited:
                continue

            if map_dict.get(new_pos) == "#":
                continue

            queue.append((new_pos, current_steps + 1))
            visited[new_pos] = current_steps + 1
            visited_list.append(new_pos)

    # Now check how many time we can cheat that saves us atleast limit number of steps
    
    # Go through all the visited nodes and check if we can cheat
    result = 0
    for index, pos in enumerate(visited_list):
        steps = visited[pos]
        x, y = pos
        
        for i in range(index + limit, len(visited_list)):
            next_pos = visited_list[i]
            next_steps = visited[next_pos]
            next_x, next_y = next_pos

            # Check manhattan distance
            manhattan = abs(x - next_x) + abs(y - next_y)
            if manhattan <= 20:
                temp_steps = steps + manhattan
                if (next_steps - temp_steps) >= limit:
                    debug_print("Can cheat from", pos, "to", next_pos, "and save", next_steps - temp_steps, "steps")
                    result += 1

    return result
    

# Test the example
result = solve(example_input, 50)
if result == example1_result:
    print()
    print("The example result matches the expected result.")
    print()
else:
    print()
    print("The example result does not match the expected result. Got:", result, "Expected:", example1_result)
    print()

# Call the function and get the problem input
problem_input = fetch_advent_input(20)

if problem_input:
    problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    start_time = time.time()
    result = solve(problem_input, 100)
    end_time = time.time()
    print()
    print("The result of this Part is:", result)
    print("Execution time was: ", end_time - start_time, "seconds.")
    print()