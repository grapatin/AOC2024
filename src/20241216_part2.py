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
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""
example1_result = 45

def solve(input_string: str) -> int:
    # Parse the input into a dict_map
    dict_map = {}
    for y, line in enumerate(input_string.split("\n")):
        for x, char in enumerate(line):
            dict_map[(x, y)] = char

    # Find the start position
    start_position = None
    for position, char in dict_map.items():
        if char == "S":
            start_position = position
            break

    # Find end position
    end_position = None
    for position, char in dict_map.items():
        if char == "E":
            end_position = position
            break

    # Find the shortest path but turns cost 1000 so we need to minimize the turns
    # and then minimize the number of steps
    # We will use a BFS to find the shortest path
    facing = (1, 0)
    visit_cords = []
    queue = [(start_position, 0, 0, 0, facing, [start_position])]

    # Always start facing right
    
    visited = dict()
    lowest_cost = 100000000
    best_spot_set = set()
    while queue:
        position, turns, steps, cost, facing, visit_cords = queue.pop(0)
        if position in visited and cost > (visited[position] + 1000):
            continue
        visited[position] = cost
        x, y = position
        if position == end_position:
            print("One hit found at cost:", cost) 
            if cost < lowest_cost:
                lowest_cost = cost
                step_count = steps
                best_spot_set = set()
                for cord in visit_cords:
                    best_spot_set.add(cord)
            elif cost == lowest_cost:
                for cord in visit_cords:
                    best_spot_set.add(cord)

        # First check if we can move forward
        # Then add 1000 to the cost and try to turn left and right
        # Forward
        next_position = (x + facing[0], y + facing[1])
        if dict_map.get(next_position) != "#":
            # do a copy that works with tuples
            queue.append((next_position, turns, steps + 1, cost + 1, facing, visit_cords + [next_position]))
        # Right
        if facing == (0, 1):
            next_facing = (-1, 0)
        elif facing == (0, -1):
            next_facing = (1, 0)
        elif facing == (1, 0):
            next_facing = (0, 1)
        elif facing == (-1, 0):
            next_facing = (0, -1)
        next_position = (x + next_facing[0], y + next_facing[1])
        if dict_map.get(next_position) != "#":
            queue.append((next_position, turns + 1, steps + 1, cost + 1001, next_facing, visit_cords + [next_position]))
        # Left
        if facing == (0, 1):
            next_facing = (1, 0)
        elif facing == (0, -1):
            next_facing = (-1, 0)
        elif facing == (1, 0):
            next_facing = (0, -1)
        elif facing == (-1, 0):
            next_facing = (0, 1)
        next_position = (x + next_facing[0], y + next_facing[1])
        if dict_map.get(next_position) != "#":
            queue.append((next_position, turns + 1, steps + 1, cost + 1001, next_facing, visit_cords + [next_position]))

    # pretty print map with all visited positions marked as 'O'
    maxX = max([cord[0] for cord in dict_map.keys()]) + 1
    maxY = max([cord[1] for cord in dict_map.keys()]) + 1
    for y in range(maxY):
        for x in range(maxX):
            if (x, y) in best_spot_set:
                print("O", end="")
            else:
                print(dict_map[(x, y)], end="")
        print()
    return len(best_spot_set)  

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
problem_input = fetch_advent_input(16)

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