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
example1_result = "co,de,ka,ta"


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
            
    # for each party remove pairs that are not directly connected
    new_parties = []
    for cpu in computers:
        done = False
        party = computer_dict[cpu]
        party.add(cpu)
        while not done:
            done = True
            # Lets count how many direct connections each computer in party has with other computers in the party
            # remove the one with lowest count
            # repeat until all computers are connected directly
            lowest_count = 100000
            lowest_cpu = ""
            for cpu1 in party:
                count = 0
                for cpu2 in party:
                    if cpu1 == cpu2:
                        continue
                    if cpu2 in computer_dict[cpu1]:
                        count += 1
                    else:
                        # We should stop if all are connected directly
                        done = False
                if count < lowest_count:
                    lowest_count = count
                    lowest_cpu = cpu1
            # Drop the computer with the lowest count
            if not done:
                party.remove(lowest_cpu)        

        new_parties.append(party)

    # Find the biggest party and sort the computer names, return it as a comma seperated string
    biggest_party = 0
    final_party = set()
    for party in new_parties:
        if len(party) > biggest_party:
            biggest_party = len(party)
            final_party = party

    final_party = sorted(final_party)

    # Now sort and comma seperate final_party
    output = ",".join(final_party)
    return output


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