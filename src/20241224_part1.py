from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


example_input = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

example1_result = 2024

def solve(input_string: str) -> int:
    start_values, instructions = input_string.split("\n\n")

    wires = {}
    for line in start_values.split("\n"):
        wire, value = line.split(": ")
        wires[wire] = int(value)

    done = False
    while not done:
        for wire in wires:
            # replace the wire with the value in the instructions
            instructions = re.sub(r"\b" + wire + r"\b", str(wires[wire]), instructions)
        done = True
        for ins in instructions.split("\n"):
            #  Check how many numbers are souronded by space in the statement
            numbers = re.findall(r"\b\d+\b", ins)
            if len(numbers) == 2:
                # We can evaluate the statement
                # Get the wire name after -> exampel kwq, z05
                wire_name = ins.split(" -> ")[1]
                if "AND" in ins:
                    wires[wire_name] = int(numbers[0]) & int(numbers[1])
                elif "XOR" in ins:
                    wires[wire_name] = int(numbers[0]) ^ int(numbers[1])
                elif "OR" in ins:
                    wires[wire_name] = int(numbers[0]) | int(numbers[1])
                done = False
            else:
                continue
            
    # print all wires alabetically
    z_binary = ""
    for wire in sorted(wires):
        if wire[0] == "z":
            z_binary += str(wires[wire])
        print(wire, wires[wire])

    # reverse the binary string
    z_binary = z_binary[::-1]
    print("Z_binary:", z_binary), "Z_decimal:", int(z_binary, 2)

    return int(z_binary, 2)




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
problem_input = fetch_advent_input(24)

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