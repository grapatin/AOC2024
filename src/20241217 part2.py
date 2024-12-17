from fetch_advent_input import fetch_advent_input
import re
import time

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

example_input = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
example1_result = 117440

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

    program_string = program.split(": ")[1]
    #Get each int in program and pass into a list
    program = list(map(int, program_string.split(",")))
    len_input_program = len(program)

    # We should try to solve this by getting same output as the program
    # each octet in A creates one output
    # lets try to solve this backwards by on the highest octet in A that creates the last output = program[-1]
    # then we can try to solve the next octet in A that creates the second last output = program[-2]
    # and so on until we have solved all outputs
    # the number of octets in A will be same as number of steps in the program
    # we can try to solve this by brute force

    #result = 8**len_input_program
    results = []
    possible_values = []
    possible_values.append(0)

    lowest_value = 8**(len_input_program + 1)
    output_solved_so_far = 0
    for octet_number in range(len_input_program):
        #lets try to solve with highest octet first
        octet_number = len_input_program - octet_number - 1
        print("Octet number:", octet_number)
        results = possible_values.copy()    

        for result_input in results:
            for k in range(8):
                start_value = k*(8**octet_number) + result_input
                registers_dict["A"] = start_value
                #registers_dict["A"] = int("0o345300", 8)
                #registers_dict["A"] = int("0o4532316267433310", 8)

                registers_dict["B"] = 0
                registers_dict["C"] = 0
                # Execute the program
                ip = 0
                output = ''
                output_list = []

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
                        output_list.append(combo_operand % 8)
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
                #check if last field in output_list is same as program[-1]
                if len(output_list) == len_input_program:
                    if output_list[len_input_program - output_solved_so_far - 1] == program[len_input_program - output_solved_so_far - 1]: 
                        #print("Output solved:", output_list[len_input_program - output_solved_so_far - 1], "output_solved_so_far:", output_solved_so_far, "current_value:", oct(start_value))   
                        possible_values.append(start_value)
                        #print(output_list)
                        #print(program)
                        #check if all values match
                        if output_list == program:
                            if start_value < lowest_value:
                                lowest_value = start_value
                                print("Lowest value so far:", oct(lowest_value))
        output_solved_so_far += 1
    return lowest_value

# Test the example
result = solve(example_input)
if result == example1_result:
    print()
    print("The example result matches the expected result.", oct(result), result)
    print()
else:
    print()
    print("The example result does not match the expected result. Got:", oct(result), "Expected:", oct(example1_result))
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