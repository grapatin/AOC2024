from fetch_advent_input import fetch_advent_input
import re
import time
import io
import zipfile

def compress_string(input_string: str) -> bytes:
    # Create an in-memory byte stream
    byte_stream = io.BytesIO()
    
    # Create a ZipFile object
    with zipfile.ZipFile(byte_stream, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Write the input string to the zip file
        zip_file.writestr('compressed_string.txt', input_string)
    
    # Get the compressed data
    compressed_data = byte_stream.getvalue()
    
    return compressed_data

def calculate_quadrants(map_dict, max_x, max_y):
    #find middle row and column

    middle_col = max_x // 2
    left_side = 0
    right_side = 0
    middle_count = 0

    for y in range(max_y):
        for x in range(max_x):
            if (x, y) in map_dict:
                if x < middle_col:
                    left_side += 1
                elif x > middle_col:
                    right_side += 1
                else:
                    middle_count += 1

    #assume summetrical left and right side
    return middle_count

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
    
def pretty_print_file(list_of_robots, max_x, max_y, n=0):
    # Pretty print robots in space and in each space print how many they are in that space
    # Create a dict map of cord system with '.' as empty space and '123' as number of robots in that space
    # Write the map to a file
    filename="output.txt"
    map_dict = {}
    for robot in list_of_robots:
        if tuple(robot.position) in map_dict:
            map_dict[tuple(robot.position)] += 1
        else:
            map_dict[tuple(robot.position)] = 1

    one_string = ""
    with open(filename, "a") as file:
        #file.write(f"Time: {n}\n")
        for y in range(max_y):
            for x in range(max_x):
                if (x, y) in map_dict:
                    #file.write(str(map_dict[(x, y)]))
                    one_string += str(map_dict[(x, y)])
                else:
                    #file.write(".")
                    one_string += "."
            #file.write("\n")
            one_string += "\n"

    return map_dict, one_string

def solve(input_string: str, max_x, max_y) -> int:
    list_of_robots = []
    #parse the input
    for line in input_string.split("\n"):
        #parse the position and velocity
        position = list(map(int, re.findall(r"-?\d+", line)[:2]))
        velocity = list(map(int, re.findall(r"-?\d+", line)[2:]))
        list_of_robots.append(Robot(position, velocity, max_x, max_y))

    n = 0
    m = 0
    max_moves = 10000
    #move the robots for max_moves times
    map_dict, one_string = pretty_print_file(list_of_robots, max_x, max_y, n)
    size = len(compress_string(one_string))
    best_move = 0
    print(f"Time: {m}", n, size)
    while n < max_moves:
        n += 1
        for robot in list_of_robots:
            robot.move()
        #check if the robots are close to each other
        if n >= 197:
            m += 1


        map_dict, one_string = pretty_print_file(list_of_robots, max_x, max_y, n)
        #compress one_string to check entropy in the string
        if len(compress_string(one_string)) < size:
            size = len(compress_string(one_string))
            print(f"Time: {m}", n, "compressed size", size, "diff", calculate_quadrants(map_dict, max_x, max_y))    
            best_move = n

    return best_move

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