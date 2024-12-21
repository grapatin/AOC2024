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


example_input = """456A"""
example1_result = 126384

class numeric_keypad:
    def __init__(self):
        keypad_layout = """789
        456
        123
        #0A"""

        self.dict_map_keypad = {}
        self.dict_map_reverse = {}
        x = 0
        y = 0
        for line in keypad_layout.split("\n"):
            for char in line:
                if char != ' ':
                    self.dict_map_keypad[(x, y)] = char
                    self.dict_map_reverse[char] = (x, y)
                    x += 1
            y += 1
            x = 0
    
        # For each 2 comp of A0123456789 create a shortest path
        # manhattan distance between the 2 points and create a L, R, U, D path

        chars = '0123456789A'
        self.shortest_paths_dict = {}
        for char1 in chars:
            for char2 in chars:
                if char1 != char2:
                    pos1 = self.dict_map_reverse[char1]
                    pos2 = self.dict_map_reverse[char2]
                    path = ""
                    if pos1[0] < pos2[0]:
                        path += 'R' * (pos2[0] - pos1[0])
                    else:
                        path += 'L' * (pos1[0] - pos2[0])

                    if pos1[1] < pos2[1]:
                        path += 'D' * (pos2[1] - pos1[1])
                    else:
                        path += 'U' * (pos1[1] - pos2[1])

                    self.shortest_paths_dict[char1 + char2] = path
                else:
                    self.shortest_paths_dict[char1 + char2] = ''

        self.current_state = 'A'
        self.current_cord = self.dict_map_reverse['A']

    def reset(self):
        self.current_state = 'A'
        self.current_cord = self.dict_map_reverse['A']

    def move(self, char_numeric):
        where_to_go = self.current_state + char_numeric
        sequence = self.shortest_paths_dict[where_to_go]
        self.current_state = char_numeric
        # also press the button
        sequence += 'A'
        return sequence
    
    def simulate(self, sequence):
        output = ''
        current_cord = self.current_cord
        for direction in sequence:
            if direction == 'U' or direction == '^':    
                current_cord = (current_cord[0], current_cord[1] - 1)
            elif direction == 'D' or direction == 'v':
                current_cord = (current_cord[0], current_cord[1] + 1)
            elif direction == 'L' or direction == '<':
                current_cord = (current_cord[0] - 1, current_cord[1])
            elif direction == 'R' or direction == '>':
                current_cord = (current_cord[0] + 1, current_cord[1])
            elif direction == 'A':
                self.current_cord = current_cord
                output += self.dict_map_keypad[current_cord]
        return output

    
class directional_keypad:
    def __init__(self):
        keypad_layout = """#UA
        LDR"""

        self.dict_map_keypad = {}
        self.dict_map_reverse = {}
        x = 0
        y = 0
        for line in keypad_layout.split("\n"):
            for char in line:
                if char != ' ':
                    self.dict_map_keypad[(x, y)] = char
                    self.dict_map_reverse[char] = (x, y)
                    x += 1
            y += 1
            x = 0
        # create a list shortest part for directional keypad
        self.shortest_paths_dict_directional = {}
        chars = 'ALRUD'
        for char1 in chars:
            for char2 in chars:
                if char1 != char2:
                    pos1 = self.dict_map_reverse[char1]
                    pos2 = self.dict_map_reverse[char2]
                    path = ""
                    if pos1[0] < pos2[0]:
                        path += 'R' * (pos2[0] - pos1[0])
                    else:
                        path += 'L' * (pos1[0] - pos2[0])
                    if pos1[1] < pos2[1]:
                        path += 'D' * (pos2[1] - pos1[1])
                    else:
                        path += 'U' * (pos1[1] - pos2[1])

                    self.shortest_paths_dict_directional[char1 + char2] = path
                else:
                    self.shortest_paths_dict_directional[char1 + char2] = ''

        self.current_state = 'A'
        self.current_cord = self.dict_map_reverse[self.current_state]

    def reset(self):
        self.current_state = 'A'
        self.current_cord = self.dict_map_reverse['A']


    def move(self, direction):
        where_to_go = self.current_state + direction
        sequence = self.shortest_paths_dict_directional[where_to_go]
        self.current_state = direction
        # also press the button
        sequence += 'A'
        return sequence
    
    def simulate(self, sequence):
        output = ''
        current_cord = self.current_cord
        for direction in sequence:
            if direction == 'U' or direction == '^':
                current_cord = (current_cord[0], current_cord[1] - 1)
            elif direction == 'D' or direction == 'v':
                current_cord = (current_cord[0], current_cord[1] + 1)
            elif direction == 'L' or direction == '<':
                current_cord = (current_cord[0] - 1, current_cord[1])
            elif direction == 'R' or direction == '>':
                current_cord = (current_cord[0] + 1, current_cord[1])
            elif direction == 'A':
                self.current_cord = current_cord
                output += self.dict_map_keypad[current_cord]
        return output
                      
def solve(input_string: str) -> int:

    # Parse the input
    keypad = numeric_keypad()
    direction_keypad1 = directional_keypad()
    direction_keypad2 = directional_keypad()

    result = 0

    # Parse the input
    for line in input_string.split("\n"):
        sequence_builder = ""
        sequence2_builder = ""
        sequence3_builder = ""
        # Parse the position and velocity
        for char in line:
            sequence = keypad.move(char)
            sequence_builder += sequence
            debug_print(f"Char: {char}, Sequence: {sequence} Sequence_builder: {sequence_builder}")
            for direction1 in sequence:
                sequence2 = direction_keypad1.move(direction1)
                sequence2_builder += sequence2
                debug_print(f"Direction: {direction1}, Sequence2: {sequence2}, Sequence2_builder: {sequence2_builder}")
                for direction2 in sequence2:
                    sequence3 = direction_keypad2.move(direction2)
                    sequence3_builder += sequence3
                    debug_print(f"Direction2: {direction2}, Sequence3: {sequence3}, Sequence3_builder: {sequence3_builder}")
                    

        # Number equals line with last char dropped
        number = int(line[:-1])

        result_dict = {}
        result_dict['029A'] = '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'
        result_dict['980A'] = '<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A'
        result_dict['179A'] = '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'
        result_dict['456A'] = '<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A'
        result_dict['379A'] = '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'
        print("Line", line, "Sequence", sequence3_builder, "number * length", len(sequence3_builder), '*', number)
        print("Line", line, "Sequence", result_dict[line], "number * length", len(result_dict[line]), '*', number)
        
        sim = sequence3_builder
        sim_keypad2 = direction_keypad2.simulate(sim)
        sim_keypad1 = direction_keypad1.simulate(sim_keypad2)
        sim_keypad = keypad.simulate(sim_keypad1)
        sim_ex = result_dict[line]
        sim_ex_keypad2 = direction_keypad2.simulate(sim_ex)
        sim_ex_keypad1 = direction_keypad1.simulate(sim_ex_keypad2)
        sim_ex_keypad = keypad.simulate(sim_ex_keypad1)

        print('number sim:', sim_keypad, sim_ex_keypad, sim_keypad == sim_ex_keypad)

        sim = '<v<A>>^AA<vA<A>>^AAvAA<^A>A'
        sim_keypad2 = direction_keypad2.simulate(sim)
        sim_keypad1 = direction_keypad1.simulate(sim_keypad2)
        sim_keypad = keypad.simulate(sim_keypad1)
        print('Short sim:', sim_keypad, 'sim_keypad1:', sim_keypad1, 'sim_keypad2:', sim_keypad2, ' sim:', sim)
        sim_ex = 'LLDAARARUAADALUARAADAUALDA'
        direction_keypad1.reset()
        direction_keypad2.reset()
        keypad.reset()
        sim_ex_keypad2 = direction_keypad2.simulate(sim_ex)
        sim_ex_keypad1 = direction_keypad1.simulate(sim_ex_keypad2)
        sim_ex_keypad = keypad.simulate(sim_ex_keypad1)
        print('Short exs:', sim_ex_keypad, 'sim_keypad1:', sim_ex_keypad1, 'sim_keypad2:', sim_ex_keypad2, 'sim:', sim_ex) 

        print
        result += len(sequence3_builder)*number 

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