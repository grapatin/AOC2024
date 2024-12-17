from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

example_input = """Register A: 0
Register B: 0
Register C: 9

Program: 2,6"""
example1_result = '4,6,3,5,6,3,5,2,1,0'

def solve(input_string: str) -> int:

    def combo_check(combo_operand: int) -> int:
        if combo_operand in (0, 1, 2, 3):
            return combo_operand
        elif combo_operand == 4:
            return registers_dict["A"]
        elif combo_operand == 5:
            return registers_dict["B"]
        elif combo_operand == 6:
            return registers_dict["C"]
        elif combo_operand == 7:
            #not supported
            return 0

    registers, program = input_string.split("\n\n")
    registers = registers.split("\n")

    registers_dict = {}
    for register in registers:
        name, value = register.split(": ")
        registers_dict[name.split(' ')[1]] = int(value)

    program = program.split(": ")[1]
    #Get each int in program and pass into a list
    program = list(map(int, program.split(",")))

    # Execute the program
    ip = 0
    output = ''

    while ip < len(program):
        instruction = program[ip]
        combo_operand = combo_check(program[ip + 1])
        literal_operand = program[ip + 1]
        if instruction == 0:
            # adv division
            numerator = registers_dict["A"]
            denominator = 2 ** combo_operand
            #result = numerator / denominator but truncated to int
            registers_dict["A"] =  numerator // denominator
        elif instruction == 1:
            # bxl bitwise xor register B and literal operand
            registers_dict["B"] ^= literal_operand 
        elif instruction == 2:
            #bst combo operand modulo 8 store in register B
            registers_dict["B"] = combo_operand % 8
        elif instruction == 3:
            # jnx instructior
            if registers_dict["A"] == 0:
                pass
            else:
                ip = literal_operand
                continue
            # leave ip to increase as normal
        elif instruction == 4:
            # bxc bitwise xor register B and register C
            registers_dict["B"] = registers_dict["B"] ^ registers_dict["C"]
        elif instruction == 5:
            # out, combo operand modulo 8
            output += str(combo_operand % 8) + ","
        elif instruction == 6:
            # bdv 
            numerator = registers_dict["A"]
            denominator =  2 ** combo_operand
            #result = numerator / denominator but truncated to int
            registers_dict["B"] = numerator // denominator
        elif instruction == 7:
            # cdv 
            numerator = registers_dict["A"]
            denominator =  2 ** combo_operand
            #result = numerator / denominator but truncated to int
            registers_dict["C"] = numerator // denominator
        ip += 2

    output = output[:-1]
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
problem_input = fetch_advent_input(17)

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