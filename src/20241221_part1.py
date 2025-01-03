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


#example_input = """456A"""
example1_result = 126384

class numeric_keypad:
    def __init__(self):
        keypad_layout = """789\n456\n123\n#0A"""

        direction_pad = directional_keypad()
        self.dict_map_keypad = {}
        self.dict_map_reverse = {}
        self.clear_text_path = {}
        x = 0
        y = 0
        for line in keypad_layout.split("\n"):
            for char in line:
                if char != '#':
                    self.dict_map_keypad[(x, y)] = char
                    self.dict_map_reverse[char] = (x, y)
                x += 1
            y += 1
            x = 0
    
        # For each 2 comp of A0123456789 create a shortest path
        chars = '0123456789A'
        self.shortest_paths_dict = {}
        for char1 in chars:
            for char2 in chars:
                # find shortest path between 2 points with BFS
                # '#' is a wall
                queue = []
                clear_text_path = ''
                start_pos = self.dict_map_reverse[char1]
                stop_pos = self.dict_map_reverse[char2]
                visited = set()
                visited.add(start_pos)
                queue.append((start_pos, '', 'A', clear_text_path))
                best_path = '##############################################################################################'
                while queue:
                    current_pos, current_path, key_pad_position, clear_text_path = queue.pop(0)
                    x, y = current_pos
                    if current_pos == stop_pos:
                        if len(current_path) < len(best_path):
                            best_path = current_path
                            self.shortest_paths_dict[char1 + char2] = best_path + 'A'
                            self.clear_text_path[char1 + char2] = clear_text_path + 'A'
                    # Add all the neighbors
                    directions = [(1, 0, 'R'), (0, -1, 'U'), (0, 1, 'D'), (-1, 0, 'L')]
                    for dx, dy, direction in directions:
                        new_x = x + dx
                        new_y = y + dy
                        new_pos = (new_x, new_y)
                        if new_pos not in visited and new_pos in self.dict_map_keypad:
                            # get the cost to move in this direction use direction_pad
                            path_to_add = direction_pad.second_level_direction[key_pad_position+direction]
                            visited.add(new_pos)
                            queue.append((new_pos, current_path + path_to_add, direction, clear_text_path + direction))

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
        keypad_layout = """#UA\nLDR"""

        self.dict_map_keypad = {}
        self.dict_map_reverse = {}
        x = 0
        y = 0
        for line in keypad_layout.split("\n"):
            for char in line:
                if char != '#':
                    self.dict_map_keypad[(x, y)] = char
                    self.dict_map_reverse[char] = (x, y)
                x += 1
            y += 1
            x = 0
        # create a list shortest part for directional keypad
        self.shortest_paths_dict_directional = {}
        self.second_level_direction = {}
        chars = 'ALRUD'
        for char1 in chars:
            for char2 in chars:
                # find shortest path between 2 points with BFS
                # '#' is a wall
                queue = []
                start_pos = self.dict_map_reverse[char1]
                stop_pos = self.dict_map_reverse[char2]
                visited = set()
                visited.add(start_pos)
                queue.append((start_pos, ''))
                while queue:
                    current_pos, current_path = queue.pop(0)
                    x, y = current_pos
                    if current_pos == stop_pos:
                        self.shortest_paths_dict_directional[char1 + char2] = current_path + 'A'
                        break
                    # Add all the neighbors
                    directions = [(0, 1, 'D'), (1, 0, 'R'), (0, -1, 'U'), (-1, 0, 'L')]
                    for dx, dy, direction in directions:
                        new_x = x + dx
                        new_y = y + dy
                        new_pos = (new_x, new_y)
                        if new_pos not in visited and new_pos in self.dict_map_keypad:
                            visited.add(new_pos)
                            queue.append((new_pos, current_path + direction))

        # now calculate the shortets path for second level, i.e. using shortest_paths_dict_directional
        # to calculate the shortest path between 2 points
        chars = 'ALRUD'
        for char1 in chars:
            for char2 in chars:
                queue = []
                start_pos = self.dict_map_reverse[char1]
                stop_pos = self.dict_map_reverse[char2]

                # get first level direction
                first_level_direction = self.shortest_paths_dict_directional[char1 + char2]
                # now start from A and go through the first level direction
                start_char = 'A'
                path = ''
                while (first_level_direction):
                    # get first char in first_level_direction and remove it
                    direction = first_level_direction[0]
                    first_level_direction = first_level_direction[1:]
                    path += self.shortest_paths_dict_directional[start_char + direction]
                    start_char = direction
                # Now find the path back to 'A'
                second_part_of_path = self.shortest_paths_dict_directional[char2 + 'A']
                while (second_part_of_path):
                    # get first char in first_level_direction and remove it
                    direction = second_part_of_path[0]
                    second_part_of_path = second_part_of_path[1:]
                    path += self.shortest_paths_dict_directional[start_char + direction]
                    start_char = direction

                self.second_level_direction[char1 + char2] = path

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
        simulated = ''
        simulated_pos = []
        simulated_pos.append(self.current_cord)
        for direction in sequence:
            simulated += direction
            if direction == 'U' or direction == '^':
                current_cord = (current_cord[0], current_cord[1] - 1)
                simulated_pos.append((current_cord[0], current_cord[1] - 1))
            elif direction == 'D' or direction == 'v':
                current_cord = (current_cord[0], current_cord[1] + 1)
                simulated_pos.append((current_cord[0], current_cord[1] + 1))
            elif direction == 'L' or direction == '<':
                current_cord = (current_cord[0] - 1, current_cord[1])
                simulated_pos.append((current_cord[0] - 1, current_cord[1]))
            elif direction == 'R' or direction == '>':
                current_cord = (current_cord[0] + 1, current_cord[1])
                simulated_pos.append((current_cord[0] + 1, current_cord[1]))
            elif direction == 'A':
                self.current_cord = current_cord
                output += self.dict_map_keypad[current_cord]
        return output
                      

def simulate_all(sequence, keypad, direction_keypad):
    output = ''

    direction_keypad.reset()
    keypad.reset()
    temp = direction_keypad.simulate(sequence)
    print("First simulation:", temp)
    direction_keypad.reset()
    temp = direction_keypad.simulate(temp)
    print("Second simulation:", temp)
    temp = keypad.simulate(temp)
    print("Third simulation:", temp)
    output = temp

    return output

def solve(input_string: str) -> int:
    # Parse the input
    keypad = numeric_keypad()
    direction_keypad1 = directional_keypad()
    direction_keypad2 = directional_keypad()

    result = 0

    # Parse the input
    for line in input_string.split("\n"):
        move_from_char = 'A'
        sequence = ''
        sequence2 = ''
        sequence3 = ''
        int_portion = int(re.findall(r"\d+", line)[0])
        if line == '379A':
            print("Line:", line, "Int portion:", int_portion)

        for move_to_char in line:
            sequence += keypad.clear_text_path[move_from_char + move_to_char]
            move_from_char = move_to_char

        print("Sequence:", sequence, "for line:", line, "length", len(sequence))

        move_from_char = 'A'

        for move_to_char in sequence:
            sequence2 += direction_keypad1.shortest_paths_dict_directional[move_from_char + move_to_char]
            move_from_char = move_to_char

        print("Sequence:", sequence2, "for line:", line, "length", len(sequence2))

        move_from_char = 'A'
        for move_to_char in sequence2:
            sequence3 += direction_keypad2.shortest_paths_dict_directional[move_from_char + move_to_char]
            move_from_char = move_to_char

        result += int_portion*len(sequence3)
        print("Sequence:", sequence3, "for line:", line, "length", len(sequence3))


    print('Simulation:', simulate_all('<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A', keypad, direction_keypad1))
    print('Simulation:', simulate_all('DLALAARRUADAAULARADLLARRUADAUADLALARRUADAAULARADLLARRUADAUAADAUAADAUA', keypad, direction_keypad2))
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