from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

example_input = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
example1_result = 7

def solve(input_string: str) -> int:
    # Parse the input
    connections = []
    computers = set()

    for line in input_string.split("\n"):
        comp1, comp2 = line.split("-")
        computers.add(comp1)
        computers.add(comp2)
        # Parse the connection
        connections.append(line.split("-"))

    set_of_parties = set()
    computer_dict = {}
    for lan1, lan2 in connections:
        if lan1 in computer_dict:
            computer_dict[lan1].add(lan2)
        else:
            computer_dict[lan1] = set()
            computer_dict[lan1].add(lan2)

        if lan2 in computer_dict:
            computer_dict[lan2].add(lan1)
        else:
            computer_dict[lan2] = set()
            computer_dict[lan2].add(lan1)

    # Find all 3 way parties, where all 3 computers are connected directly to each other
    for computer in computers:
        for second_computer in computer_dict[computer]:
            for third_computer in computer_dict[computer]:
                if second_computer != third_computer:
                    if third_computer in computer_dict[second_computer]:
                        sorted_party = sorted([computer, second_computer, third_computer])
                        set_of_parties.add(tuple(sorted_party))
    count = 0
    list_of_tuples = []
    for party in set_of_parties:
        for computer in party:
            # if name in computer contains t add to count
            if "t" == computer[0]:
                count += 1
                list_of_tuples.append(party)
                break #Making sure we only count it once even multiple computer has t in name
    
    return count

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
problem_input = fetch_advent_input(23)

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