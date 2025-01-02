from fetch_advent_input import fetch_advent_input
import re
import time
import functools

# Define a debug flag
DEBUG = False

# Custom debug print function
def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

def calculate(a, b, operator):
    if operator == "AND":
        return a & b
    elif operator == "XOR":
        return a ^ b
    elif operator == "OR":
        return a | b
    
def test_calculate_option2(instruction_list, instructions_resolved):
 
    wires = instructions_resolved

    done = False
    new_wires = {}
    for wire in wires:
        # replace the wire with the value in the instructions_list
        for index, ins in enumerate(instruction_list):
            ins = re.sub(r"\b" + wire + r"\b", str(wires[wire]), ins)
            instruction_list[index] = ins

    while not done:
        wires.update(new_wires)
        for wire in new_wires:
            # replace the wire with the value in the instructions_list
            for index, ins in enumerate(instruction_list):
                ins = re.sub(r"\b" + wire + r"\b", str(wires[wire]), ins)
                instruction_list[index] = ins

        new_wires = {}
        done = True
        for ins in instruction_list:
            #  Check how many numbers are souronded by space in the statement
            numbers = re.findall(r"\b\d+\b", ins)
            if len(numbers) == 2:
                # We can evaluate the statement
                # Get the wire name after -> exampel kwq, z05
                wire_name = ins.split(" -> ")[1]
                if "AND" in ins:
                    new_wires[wire_name] = int(numbers[0]) & int(numbers[1])
                elif "XOR" in ins:
                    new_wires[wire_name] = int(numbers[0]) ^ int(numbers[1])
                elif "OR" in ins:
                    new_wires[wire_name] = int(numbers[0]) | int(numbers[1])
                done = False
            else:
                continue
            
    # print all wires alabetically
    z_binary = ""
    for wire in sorted(wires):
        if wire[0] == "z":
            z_binary += str(wires[wire])
        #print(wire, wires[wire])

    # reverse the binary string
    z_binary = z_binary[::-1]
    return int(z_binary, 2)

def test_calculate(instructions_unresolved, instructions_resolved):
    done = False
    while not done:
        done = True
        for key in instructions_unresolved:
            a, b, operator = instructions_unresolved[key]
            if a in instructions_resolved and b in instructions_resolved:
                instructions_resolved[key] = calculate(instructions_resolved[a], instructions_resolved[b], operator)
                done = False
                del instructions_unresolved[key]
                break

    #We are done, lets calculate the result
    result = 0
    for key in instructions_resolved:
        if key[0] == "z":
            # Find int portion of the key
            n = int(key[1:])
            result += instructions_resolved[key] * 2**n
    return result

def test_calculate_specific_n(instructions_unresolved, n, verbose=True):

    instructions_resolved = {}
    # clear starting variables
    numeric_over_flow = f"{n-1:02}"
    numeric_string_target = f"{n:02}"
    numeric_string_target_next = f"{n+1:02}"

    # Set all other x and y to 0
    for i in range(0, n+1):
        instructions_resolved["x"+f"{i:02}"] = 0
        instructions_resolved["y"+f"{i:02}"] = 0

    success = True
    for z in range(2):
        for x in range(2):
            for y in range(2):
                    instructions_resolved["z"+numeric_over_flow] = z
                    instructions_resolved["x"+numeric_over_flow] = z
                    instructions_resolved["y"+numeric_over_flow] = z
                    instructions_resolved["x"+numeric_string_target] = x
                    instructions_resolved["y"+numeric_string_target] = y
                    instructions_resolved["x"+numeric_string_target_next] = 0
                    instructions_resolved["y"+numeric_string_target_next] = 0

                    # Calculate expected value
                    expected_result = x*2**n + y*2**n + z*2**(n)
                    result = test_calculate(instructions_unresolved.copy(), instructions_resolved.copy())

                    if result != expected_result:
                        success = False
                        if verbose:
                            print("Got a failure at n =", n, "Expected:", expected_result, "Got:", result, " z:", z, " x:", x, " y:", y)
                    
    if success == True and verbose:
        print("Success for n=", n)
    return success
                    
def test_all_calculate(instructions_unresolved, org_list, print_output=False, speed_test=False):
    instructions_resolved = {}
    first_failure = 0
    for n in range(1,45):
        # clear starting variables
        numeric_over_flow = f"{n-1:02}"
        numeric_string_target = f"{n:02}"
        numeric_string_target_next = f"{n+1:02}"
        #del instructions_unresolved["z"+numeric_over_flow]
    
        #create all 3-bitwise combination test data
        all_tests_succeded = True
        for z in range(2):
            for x in range(2):
                for y in range(2):
                    # store the starting values
                    #instructions_resolved = {}
                    instructions_resolved["z"+numeric_over_flow] = z
                    instructions_resolved["x"+numeric_over_flow] = z
                    instructions_resolved["y"+numeric_over_flow] = z
                    instructions_resolved["x"+numeric_string_target] = x
                    instructions_resolved["y"+numeric_string_target] = y
                    instructions_resolved["x"+numeric_string_target_next] = 0
                    instructions_resolved["y"+numeric_string_target_next] = 0

                    # Calculate expected value
                    expected_result = x*2**n + y*2**n + z*2**(n)
                    timer_start = time.time()
                    result = test_calculate(instructions_unresolved.copy(), instructions_resolved.copy())
                    timer_end = time.time()
                    diff = timer_end - timer_start
                    #print("Time for test_calculate", diff, "Time for test_calculate_option2", diff2)
                    #print("Result for test_calculate", result, "Result for test_calculate_option2", result2)
                    # revert back to original values for those that will not be overwritten
                    #result = result2

                    instructions_resolved["x"+numeric_over_flow] = 0
                    instructions_resolved["y"+numeric_over_flow] = 0
                    
                    if result != expected_result:
                        if first_failure == 0:
                            first_failure = n
                            if speed_test:
                                return first_failure
                        all_tests_succeded = False
                        if print_output:
                            print("Got a failure at n =", n, "Expected:", expected_result, "Got:", result, " z:", z, " x:", x, " y:", y)
        if all_tests_succeded and print_output:
            print("All tests succeded for n =", n)

    if print_output:
        print("First failure at n =", first_failure)
    return first_failure

def solve(input_string: str) -> int:

    swapped_instructions = []
    instructions_unresolved = {}
    # Lets try to find where the wires are crossed
    # If send in binary 1 to one X startin with 00 and increase the number
    # and see if we get the expected result
    # lets preload the wires with the values
    _, instructions = input_string.split("\n\n")

    instruction_list_org = instructions.split("\n")
    complete_list_of_outputs = []
    for ins in instruction_list_org:
        input, output = ins.split(" -> ")
        if 'AND' in input:
            z, x = input.split(" AND ")
            operator = "AND"
        elif 'XOR' in input:
            z, x = input.split(" XOR ")
            operator = "XOR"
        elif 'OR' in input:
            z, x = input.split(" OR ")
            operator = "OR"
        instructions_unresolved[output] = (z, x, operator)
        complete_list_of_outputs.append(output)
    instructions_unresolved = dict(sorted(instructions_unresolved.items()))

    start_time = time.time()
    for test_n in range(1, 45):
        test_calculate_specific_n(instructions_unresolved.copy(), test_n)
    end_time = time.time()
    print("Time for test_calculate_specific_n", end_time - start_time)

    org_copy_unresolved = instructions_unresolved.copy()

    start_time = time.time()
    first_failure = test_all_calculate(instructions_unresolved, instruction_list_org, True, False)
    end_time = time.time()
    print("Time for test_all_calculate", end_time - start_time)

    ############################
    # Temp code to find the first failure at 36 instead of 11
    first_failure_list = [36, 33, 28, 11]

    for loops in range(4):
        # Randomly swap to unresolved outputs with each other
        best_result = 0
        best_swap1 = ""
        best_swap2 = ""
        first_failure = first_failure_list[loops]
        
        for i in range(len(complete_list_of_outputs)):
            print("tick, i =", i)
            output1 = complete_list_of_outputs[i]
            for j in range(i+1, len(complete_list_of_outputs)):
                output2 = complete_list_of_outputs[j]
                if output1 != output2:
                    attempt_first_failure = first_failure
                    #print(i, j, len(complete_list_of_outputs), output1, output2)
                    instructions_unresolved = org_copy_unresolved.copy()
                    instructions_unresolved[output1], instructions_unresolved[output2] = instructions_unresolved[output2], instructions_unresolved[output1]
                    #attempt_first_failure = test_all_calculate(instructions_unresolved, instruction_list_org, False, True)
                    did_it_work = test_calculate_specific_n(instructions_unresolved.copy(), first_failure, False)
                    if did_it_work:
                        print("Found a possible swap", output1, output2, attempt_first_failure)
                        all_tests_succeded = True
                        for test_n in range(first_failure, 45):
                            if not test_calculate_specific_n(instructions_unresolved.copy(), test_n):
                                all_tests_succeded = False
                                break
                        if all_tests_succeded:
                            best_swap1 = output1
                            best_swap2 = output2

                    if attempt_first_failure > first_failure:
                        first_failure = attempt_first_failure
                        best_result = first_failure
                        best_swap1 = output1
                        best_swap2 = output2
                        print("Found a possible swap", output1, output2, attempt_first_failure)
                    
        # Now permatly do the best swap and continue
        print("Best result", best_result, best_swap1, best_swap2)
        swapped_instructions.append(best_swap1)
        swapped_instructions.append(best_swap2)
        org_copy_unresolved[best_swap1], org_copy_unresolved[best_swap2] = org_copy_unresolved[best_swap2], org_copy_unresolved[best_swap1]

        for test_n in range(1, 45):
            test_calculate_specific_n(org_copy_unresolved.copy(), test_n)

    
    where_it_fails = test_all_calculate(org_copy_unresolved, True, False)


    # return swapped_instructions as a comma seperated string
    returnstring = ",".join(sorted(swapped_instructions))
    return returnstring


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