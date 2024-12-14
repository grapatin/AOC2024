from fetch_advent_input import fetch_advent_input
import re

example_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
example1_result = 18

def solve(input_string: str) -> int:
    #convert input to dictionary
    input_dict = {}
    for i, line in enumerate(input_string.split("\n")):
        for j, char in enumerate(line):
            input_dict[(i,j)] = char

    string_to_find = "XMAS"
    total = 0
    #for each pos search in all directions for 3 additional steps and see if it is possible to form the string
    #go through dictionary and check if the string can be formed
    #create list of all possible positions including diagonals
    directions = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    for pos in input_dict.keys():
        if input_dict[pos] == "X":
            for direction in directions:
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if new_pos in input_dict.keys() and input_dict[new_pos] == "M":
                    new_pos2 = (new_pos[0] + direction[0], new_pos[1] + direction[1])
                    if new_pos2 in input_dict.keys() and input_dict[new_pos2] == "A":
                        new_pos3 = (new_pos2[0] + direction[0], new_pos2[1] + direction[1])
                        if new_pos3 in input_dict.keys() and input_dict[new_pos3] == "S":
                            total += 1
    return total

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
problem_input = fetch_advent_input(4)

if problem_input:
    problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    result = solve(problem_input)
    print()
    print("The result of this Part is:", result)
    print()