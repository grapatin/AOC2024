from fetch_advent_input import fetch_advent_input
import re

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

example_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
example1_result = 123

def solve(input_string: str) -> int:
    sum_middle_number = 0
    rules, row_input = input_string.split('\n\n')

    #parse rules, create a list of tuples
    rules_list = []
    for rule in rules.split('\n'):
        rules_list.append(tuple(map(int, rule.split('|'))))

    #parse row_input, create a list of lists
    row_input_list = []
    for row in row_input.split('\n'):
        #get each number in row to create a new list
        temp_list = []
        for num in row.split(','):
            temp_list.append(int(num))
        row_input_list.append(temp_list)
        
    incorrect_documents = []
    #for each row in row_input_list, check if all rules are satisfied
    for row in row_input_list:
        rules_correct = True
        for rule in rules_list:
            #tuple part1 if in row bust before part2 if in row
            if rule[0] in row and rule[1] in row:
                #now check order of them
                if row.index(rule[0]) > row.index(rule[1]):
                    #fail
                    rules_correct = False
                    incorrect_documents.append(row)

                    row = check_and_swap(rules_list, row)
                    debug_print('row:', row)
                    middle_index = len(row) // 2
                    sum_middle_number += row[middle_index]
                    break

    return sum_middle_number

def check_and_swap(rules_list, row):
    not_follow_rule = True
    while (not_follow_rule):
        passed_all_test = True
        for rule in rules_list:
            #tuple part1 if in row bust before part2 if in row
            if rule[0] in row and rule[1] in row:
                #now check order of them
                pos_a = row.index(rule[0])
                pos_b = row.index(rule[1])

                if pos_a > pos_b:
                    #fail
                    debug_print('Offending Rule', rule[0], rule[1])
                    #passed_checks = False
                    row[pos_a], row[pos_b] = row[pos_b], row[pos_a]
                    passed_all_test = False
                    break #need to restart check
        
        if passed_all_test:
            not_follow_rule = False
    return row
      

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
problem_input = fetch_advent_input(5)

if problem_input:
    problem_input = problem_input.strip()
    # Use the problem_input variable as needed
    result = solve(problem_input)
    print()
    print("The result of this Part is:", result)
    print()