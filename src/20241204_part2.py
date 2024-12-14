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
example1_result = 9

def solve(input_string: str) -> int:
    #convert input to dictionary
    input_dict = {}
    new_dict = {}
    for i, line in enumerate(input_string.split("\n")):
        for j, char in enumerate(line):
            input_dict[(i,j)] = char

    total = 0

    word_to_find_dict_rev1 = {(1,-1):"M",(-1,1):"S",(-1,-1):"M",(1,1):"S"}
    word_to_find_dict_rev2 = {(1,-1):"S",(-1,1):"M",(-1,-1):"M",(1,1):"S"}
    word_to_find_dict_rev3 = {(1,-1):"S",(-1,1):"M",(-1,-1):"S",(1,1):"M"}
    word_to_find_dict_rev4 = {(1,-1):"M",(-1,1):"S",(-1,-1):"S",(1,1):"M"}



    #for each pos first find letter A
    #then check if word_to_find_dict can be found in the correct directions
    for pos in input_dict.keys():
        if input_dict[pos] == "A":
            found = True
            #get the char in word_to_find_dict and it relative position
            for direction, char in word_to_find_dict_rev1.items():
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if new_pos in input_dict.keys() and input_dict[new_pos] == char:
                    #add to new_dict
                    new_dict[new_pos] = char
                else:
                    found = False
                    break
            if found:
                new_dict[pos] = "A"
                total += 1
            
            found = True
            #get the char in word_to_find_dict and it relative position
            for direction, char in word_to_find_dict_rev2.items():
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if new_pos in input_dict.keys() and input_dict[new_pos] == char:
                    #add to new_dict
                    new_dict[new_pos] = char
                else:
                    found = False
                    break
            if found:
                new_dict[pos] = "A"
                total += 1

            found = True
            #get the char in word_to_find_dict and it relative position
            for direction, char in word_to_find_dict_rev3.items():
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if new_pos in input_dict.keys() and input_dict[new_pos] == char:
                    #add to new_dict
                    new_dict[new_pos] = char
                else:
                    found = False
                    break
            if found:
                new_dict[pos] = "A"
                total += 1

            found = True
            #get the char in word_to_find_dict and it relative position
            for direction, char in word_to_find_dict_rev4.items():
                new_pos = (pos[0] + direction[0], pos[1] + direction[1])
                if new_pos in input_dict.keys() and input_dict[new_pos] == char:
                    #add to new_dict
                    new_dict[new_pos] = char
                else:
                    found = False
                    break
            if found:
                new_dict[pos] = "A"
                total += 1

    #pretty print the new_dict as input
    for i in range(10):
        for j in range(10):
            if (i,j) in new_dict.keys():
                print(new_dict[(i,j)], end="")
            else:
                print(" ", end="")
        print()

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