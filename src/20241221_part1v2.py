from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

example_input = """029A
980A
179A
456A
379A"""
example1_result = 126384

def pretty_print_map_dict(map_dict):
    #find max x and y
    max_x = 0
    max_y = 0
    for x, y in map_dict.keys():
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    one_string = ""
    for y in range(max_y+1):
        for x in range(max_x+1):
            if (x, y) in map_dict:
                one_string += str(map_dict[(x, y)])
            else:
                one_string += "#"
        one_string += "\n"
    print(one_string)

class numeric_keypad:
    def __init__(self, connect_to_object=None, name=""):
        self.name = name
        self.connect_to_object = connect_to_object
        self.map = """789\n456\n123\n#0A"""
        self.map_dict = {}
        self.reverse_dict = {}
        # Create a dictionary of the keypad
        for y, line in enumerate(self.map.split("\n")):
            for x, char in enumerate(line):
                if char != "#":
                    self.map_dict[(x,y)] = char
                    self.reverse_dict[char] = (x,y)

        # find position of A
        for pos, char in self.map_dict.items():
            if char == "A":
                self.A = pos
        self.current_pos = self.A
        self.pressed_chars = ""
        self.shortest_paths_dict = {}
        self.shortest_paths_dict = self.find_all_shortest_path()

    def find_all_shortest_path(self):
        shortest_paths_dict = {}
        nodes = "0123456789A"
        # Lets find all shortest paths between all chars in nodes
        map = self.map_dict
        
        for i in range (len(nodes)):
            for j in range(len(nodes)):
                best_so_far = 9
                best_number_of_turns = 9
                start_node = nodes[i]
                start_pos = self.reverse_dict[start_node]
                target_node = nodes[j]
                shortest_paths_dict[start_node+","+target_node] = []
                queue = []
                queue.append((start_pos,""))
                while queue:
                    current_pos, path = queue.pop()
                    current_symbol = map[current_pos]
                    if len(path) <= best_so_far:
                        if current_symbol == target_node:
                            # Check number of times we have a change of direction
                            number_of_turns = 0
                            if len(path) > 0:
                                start_direction = path[0]
                                for direction in path:
                                    if direction != start_direction:
                                        number_of_turns += 1
                                        start_direction = direction
                            else:
                                number_of_turns = 0
                            if len(path) < best_so_far:
                                best_so_far = len(path)
                                best_number_of_turns = number_of_turns
                                shortest_paths_dict[start_node+","+target_node] = []
                                shortest_paths_dict[start_node+","+target_node].append(path + "A")
                            elif len(path) == best_so_far and number_of_turns <= best_number_of_turns:
                                if number_of_turns < best_number_of_turns:
                                    best_so_far = len(path)
                                    best_number_of_turns = number_of_turns
                                    shortest_paths_dict[start_node+","+target_node] = []
                                best_number_of_turns = number_of_turns
                                shortest_paths_dict[start_node+","+target_node].append(path + "A")
                        else:
                            # Try to move in all directions
                            directions = "<>^v"
                            for direction in directions:
                                new_pos = current_pos
                                if direction == "^":
                                    new_pos = (current_pos[0], current_pos[1]-1)
                                elif direction == "v":
                                    new_pos = (current_pos[0], current_pos[1]+1)
                                elif direction == "<":
                                    new_pos = (current_pos[0]-1, current_pos[1])
                                elif direction == ">":
                                    new_pos = (current_pos[0]+1, current_pos[1])
                                if new_pos in map:
                                    queue.append((new_pos, path+direction))
        return shortest_paths_dict
                        
    def move(self, direction):
        new_pos = self.current_pos
        if direction == "^":
            new_pos = (self.current_pos[0], self.current_pos[1]-1)
        elif direction == "v":
            new_pos = (self.current_pos[0], self.current_pos[1]+1)
        elif direction == "<":
            new_pos = (self.current_pos[0]-1, self.current_pos[1])
        elif direction == ">":
            new_pos = (self.current_pos[0]+1, self.current_pos[1])
        elif direction == "A":
            # we should print current position and return current position char
            command_sent = self.map_dict[self.current_pos]
            self.pressed_chars += command_sent
            return True
        else:
            print("Invalid direction:", direction)
            assert False
        if self.current_pos not in self.map_dict:
            # invalid move, return to previous position
            return False
        else:
            self.current_pos = new_pos
            return True

    def pretty_print(self):
        pretty_print_map_dict(self.map_dict)

class directional_keypad:
    def __init__(self, connect_to_object=None, name=""):
        self.connect_to_object = connect_to_object
        self.name = name
        self.map = """#^A\n<v>"""
        self.map_dict = {}
        self.reverse_dict = {}

        # Create a dictionary of the keypad
        for y, line in enumerate(self.map.split("\n")):
            for x, char in enumerate(line):
                if char != "#":
                    self.map_dict[(x,y)] = char
                    self.reverse_dict[char] = (x,y)
        # find position of A
        for pos, char in self.map_dict.items():
            if char == "A":
                self.A = pos
        self.current_pos = self.A
        self.command_sent = ""
        self.shortest_paths_dict = {}
        self.shortest_paths_dict = self.find_all_shortest_path()
        #print("Shortest paths dict:", self.shortest_paths_dict)
        self.shortest_paths_dict_level2 = {}
        self.shortest_paths_dict_level2 = self.find_all_shortest_path_level2()
        #print("Shortest paths dict level 2:", self.shortest_paths_dict_level2)


    def move(self, direction):
        new_pos = self.current_pos
        if direction == "^":
            new_pos = (self.current_pos[0], self.current_pos[1]-1)
        elif direction == "v":
            new_pos = (self.current_pos[0], self.current_pos[1]+1)
        elif direction == "<":
            new_pos = (self.current_pos[0]-1, self.current_pos[1])
        elif direction == ">":
            new_pos = (self.current_pos[0]+1, self.current_pos[1])
        elif direction == "A":
            # we should print current position and return current position char
            current_char = self.map_dict[self.current_pos]
            self.command_sent += current_char
            status = self.connect_to_object.move(current_char)
            return status
        else:
            print("Invalid direction:", direction)
            assert False
        if new_pos not in self.map_dict:
            # invalid move, return to previous position
            return False
        else:
            self.current_pos = new_pos
            return True

    def find_all_shortest_path(self):
        shortest_paths_dict = {}
        nodes = "<>^vA"
        # Lets find all shortest paths between all chars in nodes
        map = self.map_dict
        
        for i in range (len(nodes)):
            for j in range(len(nodes)):
                best_so_far = 9
                start_node = nodes[i]
                start_pos = self.reverse_dict[start_node]
                target_node = nodes[j]
                shortest_paths_dict[start_node+","+target_node] = []
                queue = []
                queue.append((start_pos,""))
                while queue:
                    current_pos, path = queue.pop()
                    current_symbol = map[current_pos]
                    if len(path) <= best_so_far:
                        if current_symbol == target_node:
                            if len(path) < best_so_far:
                                best_so_far = len(path)
                                shortest_paths_dict[start_node+","+target_node] = []
                                shortest_paths_dict[start_node+","+target_node].append(path + "A")
                            elif len(path) == best_so_far:
                                shortest_paths_dict[start_node+","+target_node].append(path + "A")
                        else:
                            # Try to move in all directions
                            directions = "<>^v"
                            for direction in directions:
                                new_pos = current_pos
                                if direction == "^":
                                    new_pos = (current_pos[0], current_pos[1]-1)
                                elif direction == "v":
                                    new_pos = (current_pos[0], current_pos[1]+1)
                                elif direction == "<":
                                    new_pos = (current_pos[0]-1, current_pos[1])
                                elif direction == ">":
                                    new_pos = (current_pos[0]+1, current_pos[1])
                                if new_pos in map:
                                    queue.append((new_pos, path+direction))
        return shortest_paths_dict

    def find_all_shortest_path_level2(self):
        # Find all shortest paths between all chars in map_dict
        shortest_paths_dict_level2 = {}
        nodes = "<>^vA"
        # Lets find all shortest paths between all chars in nodes
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                # start by fetching previous reslust
                possible_paths = self.shortest_paths_dict[nodes[i]+","+nodes[j]]
                best_length = 99
                for queue in possible_paths:
                    symbols_to_type = [""]
                    start_pos = "A"
                    while queue:
                        next_symbol = queue[0]
                        queue = queue[1:]
                        possible_sequences = self.shortest_paths_dict[start_pos+","+next_symbol]
                        # Create all combinations of concatenated elements
                        symbols_to_type = [x + y for x in symbols_to_type for y in possible_sequences]
                        start_pos = next_symbol
                    # keep all that have the same length
                    for sequence in symbols_to_type:
                        if len(sequence) < best_length:
                            best_length = len(sequence)
                            shortest_paths_dict_level2[nodes[i]+","+nodes[j]] = []
                            shortest_paths_dict_level2[nodes[i]+","+nodes[j]].append(sequence)
                        elif len(sequence) == best_length:
                            shortest_paths_dict_level2[nodes[i]+","+nodes[j]].append(sequence)
        return shortest_paths_dict_level2 

    def pretty_print(self):
        pretty_print_map_dict(self.map_dict)

def find_shortest_path_between_numpad_and_keypad(numpad, keypad):
    shortest_paths_dict = {}
    nodes = "0123456789A"
    for i in range (len(nodes)):
        for j in range (len(nodes)):
            print("Finding path between:", nodes[i], nodes[j])
            possible_paths = numpad.shortest_paths_dict[nodes[i]+","+nodes[j]]
            best_length = 300

            for queue in possible_paths:
                symbols_to_type = [""]
                start_pos = "A"
                while queue:
                    next_symbol = queue[0]
                    queue = queue[1:]
                    possible_sequences = keypad.shortest_paths_dict_level2[start_pos+","+next_symbol]
                    # Create all combinations of concatenated elements
                    symbols_to_type = [x + y for x in symbols_to_type for y in possible_sequences]
                    start_pos = next_symbol
                # keep all that have the same length
                for sequence in symbols_to_type:
                    if len(sequence) < best_length:
                        best_length = len(sequence)
                        shortest_paths_dict[nodes[i]+","+nodes[j]] = []
                        shortest_paths_dict[nodes[i]+","+nodes[j]].append(sequence)
                    elif len(sequence) == best_length:
                        shortest_paths_dict[nodes[i]+","+nodes[j]].append(sequence)
    return shortest_paths_dict

def solve(input_string: str) -> int:
    solution = 0
    # Create a keypad object
    num_keypad = numeric_keypad("numeric_keypad", "The numeric keypad")
    dir_keypad_next_to_numpad = directional_keypad(num_keypad, "dir_keypad_next_to_numpad")

    # Find the shortest paths between the two keys
    shortest_paths_dict = find_shortest_path_between_numpad_and_keypad(num_keypad, dir_keypad_next_to_numpad)

    for row in input_string.split("\n"):
        sequence_to_press = ""
        start_char = "A"
        for char in row:
            sequence_to_press += shortest_paths_dict[start_char+","+char][0]
            #print("From:", start_char, "To:", char, "Sequence:", shortest_paths_dict[start_char+","+char][0])
            start_char = char
        print("For:", row,"Sequence to press:", sequence_to_press, "Length:", len(sequence_to_press))     
        #execute_sequence(sequence_to_press)     
        solution += len(sequence_to_press)*int(row.split("A")[0])

    return solution
        
def execute_sequence(sequence):
    num_keypad = numeric_keypad("numeric_keypad", "The numeric keypad")
    dir_keypad_next_to_numpad = directional_keypad(num_keypad, "dir_keypad_next_to_numpad")
    #dir_keypad_next_keypad = directional_keypad(dir_keypad_next_to_numpad, "dir_keypad_next_keypad")
    dir_keypad_next_to_me = directional_keypad(dir_keypad_next_to_numpad, "dir_keypad_next_to_me")
    pressed_sequence = ""

    for direction in sequence:
        pressed_sequence += direction
        status = dir_keypad_next_to_me.move(direction)
        if not status:
            assert False
    # Print status of keyboards
    print("I have pressed:", pressed_sequence)
    print("Robot 1 have  :", dir_keypad_next_to_me.command_sent)
    print("Robot 2 have  :", dir_keypad_next_to_numpad.command_sent)
    print("Numeric keys  :", num_keypad.pressed_chars)
    return status, num_keypad.pressed_chars

test_sequence = "<vA<AA>>^AvAA<^A>A"
execute_sequence(test_sequence)
test_sequence = "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
execute_sequence(test_sequence)
test_sequence = "v<<A>A<A>^>AvAA^<A>A"
execute_sequence(test_sequence)
test_sequence = "v<<A>A<A>^>AvAA^<A>Av<<A>^>AvA^Av<<A>^>AAvA<A^>A<A>Av<<A>A^>AAAvA^<A>A"
execute_sequence(test_sequence)
# test_sequence = "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A"
# execute_sequence(test_sequence)
# test_sequence = "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"
# execute_sequence(test_sequence)
# test_sequence = "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A"
# execute_sequence(test_sequence)
# test_sequence = "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"
# execute_sequence(test_sequence)

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
problem_input = fetch_advent_input(21)

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