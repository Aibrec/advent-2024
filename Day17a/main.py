import time
import re
from collections import defaultdict

file_path = 'input.txt'

start_time = time.perf_counter()
with open(file_path, 'r') as file:
    input = []
    for line in file:
        input.append(line.strip())

# A=0, B=1, C=2
registers = [0,0,0]
for i in range(3):
    line = input[i]
    match = re.match('.*: (\d+)', line).groups()
    registers[i] = int(match[0])

program = list(int(c) for c in input[4].split(' ')[1].split(','))
instruction_pointer = 0

def combo_operand(operand, registers):
    if operand >= 4:
        return registers[operand-4]
    else:
        return operand

def run_program(registers, program):
    instruction_pointer = 0
    output = []
    while instruction_pointer < len(program):
        instruction = program[instruction_pointer]
        operand = program[instruction_pointer+1]

        match instruction:
            case 0: # adv
                operand = combo_operand(operand, registers)
                numerator = registers[0]
                denominator = 2**operand
                registers[0] = numerator // denominator
            case 1: # bxl
                registers[1] = registers[1] ^ operand
            case 2: # bst
                operand = combo_operand(operand, registers)
                registers[1] = operand % 8
            case 3: # jnz
                if registers[0] != 0:
                    instruction_pointer = operand - 2
            case 4: # bxc
                registers[1] = registers[1] ^ registers[2]
            case 5: # out
                operand = combo_operand(operand, registers)
                output.append(str(operand % 8))
            case 6: # bdv
                operand = combo_operand(operand, registers)
                numerator = registers[0]
                denominator = 2 ** operand
                registers[1] = numerator // denominator
            case 7: # cdv
                operand = combo_operand(operand, registers)
                numerator = registers[0]
                denominator = 2 ** operand
                registers[2] = numerator // denominator
            case _:
                raise ValueError("Invalid instruction")

        instruction_pointer += 2
    return output, registers

output, registers = run_program(registers, program)
end_time = time.perf_counter()
print(f"Output: {"".join(output)}")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
