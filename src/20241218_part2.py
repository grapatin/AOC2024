from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
example1_result = "6,1"

def maze_solver(map_dict, start_pos, end_pos):
        
    # Solve the maze with BFS
    queue = []
    queue.append((start_pos, 0))
    visited = set()
    visited.add(start_pos)

    while queue:
        current_pos, current_steps = queue.pop(0)
        x, y = current_pos

        if current_pos == end_pos:
            return current_steps

        # Check the neighbors
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x = x + dx
            new_y = y + dy
            new_pos = (new_x, new_y)

            if new_pos in map_dict and new_pos not in visited and map_dict[new_pos] != "#":
                visited.add(new_pos)
                queue.append((new_pos, current_steps + 1))

    return -1


def solve(input_string: str, size_of_maze, number_of_obstacels) -> int:
    # Create a map_dict with number of obstacles added as walls
    # Add . for all other places with the size_of_maze
    map_dict = {}
    x = 0
    y = 0

    start_pos = (0,0)
    end_pos = (size_of_maze-1, size_of_maze-1)

    number_of_lines = input_string.count("\n")
    input_list = input_string.split("\n")

    # We need to figure out when maze is no longer possible to solve
    # Lets do it by devide and conquer
    number_obstacels_known_to_work = number_of_obstacels
    number_obstacels_known_not_to_work = number_of_lines
    while True:
        obstacels_to_test  = (number_obstacels_known_not_to_work + number_obstacels_known_to_work) // 2

        for x in range(size_of_maze):
            for y in range(size_of_maze):
                map_dict[(x, y)] = "."

        for i in range (obstacels_to_test):
            x, y = map(int, input_string.split("\n")[i].split(","))
            map_dict[(x, y)] = "#"
        if maze_solver(map_dict, start_pos, end_pos) == -1:
            number_obstacels_known_not_to_work = obstacels_to_test
            print("Number of obstacles known not to work:", number_obstacels_known_not_to_work)
            # We need remove half the obstacles
        else:
            number_obstacels_known_to_work = obstacels_to_test
            print("Number of obstacles known to work:", number_obstacels_known_to_work)
            # We need to add half the obstacles
        if number_obstacels_known_to_work - number_obstacels_known_not_to_work == -1:
            # return that line of input
            print("We are done, we have found the solution", number_obstacels_known_not_to_work)
            return input_list[number_obstacels_known_not_to_work-1]


# Test the example
result = solve(example_input, 7, 12)
if result == example1_result:
    print()
    print("The example result matches the expected result.")
    print()
else:
    print()
    print("The example result does not match the expected result. Got:", result, "Expected:", example1_result)
    print()

# Call the function and get the problem input
problem_input = fetch_advent_input(18)

if problem_input:
    problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    start_time = time.time()
    result = solve(problem_input, 71, 1024)
    end_time = time.time()
    print()
    print("The result of this Part is:", result)
    print("Execution time was: ", end_time - start_time, "seconds.")
    print()