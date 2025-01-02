import functools
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
                best_number_of_turns = 9
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

global global_keypad 
global_keypad = directional_keypad()

# Lets do recursive variant of keypad shortest path but only care about length
@functools.lru_cache(maxsize=None)
def recursive_shortest_path(start_pos, target_pos, depth):
    possible_paths = global_keypad.shortest_paths_dict[start_pos+","+target_pos]
    if depth == 0:
        return len(possible_paths[0]), ""
    else:
        best_length = -1
        for path in possible_paths:
            path_length = 0
            path_sequence = ""
            start_pos = "A"
            while path:
                next_symbol = path[0]
                path = path[1:]
                part_length, part_sequence = recursive_shortest_path(start_pos, next_symbol, depth-1)
                path_length += part_length
                path_sequence += part_sequence
                start_pos = next_symbol
            if best_length == -1:
                best_path = path_sequence
                best_length = path_length
            elif path_length < best_length:
                best_path = path_sequence
                best_length = path_length
        return best_length, ""

def find_shortest_path_between_numpad_and_keypad_rec(numpad, keypad):
    levels = 25
    nodes = "0123456789A"
    result_dict_len = {}
    result_dict_seq = {}

    for i in range (len(nodes)):
        for j in range (len(nodes)):
            possible_paths = numpad.shortest_paths_dict[nodes[i]+","+nodes[j]]
            #print("Finding path between:", nodes[i], nodes[j])
            best_length = -1
            best_path = ""
            for queue in possible_paths:
                queue_path = ""
                queue_length = 0
                start_pos = "A"
                while queue:
                    next_symbol = queue[0]
                    queue = queue[1:]
                    q_length, q_path = recursive_shortest_path(start_pos, next_symbol, levels - 1)
                    queue_length += q_length
                    queue_path += q_path
                    start_pos = next_symbol
                if best_length == -1:
                    best_path = queue_path
                    best_length = queue_length
                elif queue_length < best_length:
                    best_path = queue_path
                    best_length = queue_length
                result_dict_len[nodes[i]+","+nodes[j]] = best_length
            result_dict_seq[nodes[i]+","+nodes[j]] = best_path
    return result_dict_len, "result_dict_seq"

def solve_rec(input_string: str) -> int:
    solution = 0
    # Create a keypad object
    num_keypad = numeric_keypad("numeric_keypad", "The numeric keypad")
    dir_keypad_next_to_numpad = directional_keypad(num_keypad, "dir_keypad_next_to_numpad")

    # Find the shortest paths between the two keys
    shortest_paths_dict_rec_len, shortest_path_dict_rec_seq = find_shortest_path_between_numpad_and_keypad_rec(num_keypad, dir_keypad_next_to_numpad)

    for row in input_string.split("\n"):
        length = 0
        start_char = "A"
        for char in row:
            length += shortest_paths_dict_rec_len[start_char+","+char]
            start_char = char
        print("For:", row, "Length:", length)     
        solution += length*int(row.split("A")[0])

    return solution

# Call the function and get the problem input
problem_input = fetch_advent_input(21)

if problem_input:
    problem_input = problem_input.strip()
    start_time = time.time()
    result = solve_rec(problem_input)
    end_time = time.time()
    print()
    print("The result of this Part is:", result)
    print("Execution time was: ", end_time - start_time, "seconds.")
    print()