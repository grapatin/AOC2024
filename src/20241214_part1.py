from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
example1_result = 12

#creata a robot class to hold the position and velocity of each robot
class Robot:
    def __init__(self, position, velocity, max_x, max_y):
        self.position = position
        self.velocity = velocity
        self.max_x = max_x
        self.max_y = max_y

    def move(self):
        #wrap around max sizes also
        self.position[0] = (self.position[0] + self.velocity[0]) % self.max_x
        self.position[1] = (self.position[1] + self.velocity[1]) % self.max_y
        
    def __str__(self):
        return f"Position: {self.position}, Velocity: {self.velocity}"
    
def pretty_print_file(list_of_robots, max_x, max_y, filename="output.txt"):
    # Pretty print robots in space and in each space print how many they are in that space
    # Create a dict map of cord system with '.' as empty space and '123' as number of robots in that space
    # Write the map to a file
    map_dict = {}
    for robot in list_of_robots:
        if tuple(robot.position) in map_dict:
            map_dict[tuple(robot.position)] += 1
        else:
            map_dict[tuple(robot.position)] = 1

    with open(filename, "w") as file:
        for y in range(max_y):
            for x in range(max_x):
                if (x, y) in map_dict:
                    file.write(str(map_dict[(x, y)]))
                else:
                    file.write(".")
            file.write("\n")

    return map_dict

def solve(input_string: str, max_x, max_y) -> int:
    list_of_robots = []
    #parse the input
    for line in input_string.split("\n"):
        #parse the position and velocity
        position = list(map(int, re.findall(r"-?\d+", line)[:2]))
        velocity = list(map(int, re.findall(r"-?\d+", line)[2:]))
        list_of_robots.append(Robot(position, velocity, max_x, max_y))

    n = 0
    max_moves = 100
    #move the robots for max_moves times
    while n < max_moves:
        n += 1
        for robot in list_of_robots:
            robot.move()
        #check if the robots are close to each other
        
    map_dict = pretty_print_file(list_of_robots, max_x, max_y)

    #Split the map into 4 quadrant and drop the middle line between the quadrants
    #count the number of robots in each quadrant

    #find middle row and column
    middle_row = max_y // 2
    middle_col = max_x // 2
    quadrant1 = 0
    quadrant2 = 0
    quadrant3 = 0
    quadrant4 = 0
    for y in range(max_y):
        for x in range(max_x):
            if x < middle_col and y < middle_row:
                if (x, y) in map_dict:
                    quadrant1 += map_dict[(x, y)]
            elif x > middle_col and y < middle_row:
                if (x, y) in map_dict:
                    quadrant2 += map_dict[(x, y)]
            elif x < middle_col and y > middle_row:
                if (x, y) in map_dict:
                    quadrant3 += map_dict[(x, y)]
            elif x > middle_col and y > middle_row:
                if (x, y) in map_dict:
                    quadrant4 += map_dict[(x, y)]
    return quadrant1*quadrant2*quadrant3*quadrant4





# Test the example
result = solve(example_input, 11, 7)
if result == example1_result:
    print()
    print("The example result matches the expected result.")
    print()
else:
    print()
    print("The example result does not match the expected result. Got:", result, "Expected:", example1_result)
    print()

# Call the function and get the problem input
problem_input = fetch_advent_input(14)

if problem_input:
    problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    start_time = time.time()
    result = solve(problem_input, 101, 103)
    end_time = time.time()
    print()
    print("The result of this Part is:", result)
    print("Execution time was: ", end_time - start_time, "seconds.")
    print()