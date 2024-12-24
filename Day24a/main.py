import time
import networkx as nx
import itertools

file_path = 'input.txt'

start_time = time.perf_counter()
with open(file_path, 'r') as file:
    wires = {}
    for line in file:
        if line == '\n':
            break

        (wire, value) = line.strip().split(': ')
        wires[wire] = int(value)

    operations = []
    for line in file:
        (operation, output) = line.strip().split(' -> ')
        (left, op, right) = operation.split(' ')
        operations.append((left, right, op, output))

remaining_operations = []
while operations:
    for i, operation in enumerate(operations):
        (left, right, op, output) = operation
        if left in wires and right in wires:
            match op:
                case 'AND':
                    wires[output] = wires[left] and wires[right]
                case 'OR':
                    wires[output] = wires[left] or wires[right]
                case 'XOR':
                    wires[output] = wires[left] ^ wires[right]
        else:
            remaining_operations.append(operation)
    operations = remaining_operations
    remaining_operations = []
    #print(f"Done with {len(remaining_operations)} remaining")

z_wires = [key for key in wires.keys() if key.startswith('z')]
z_wires.sort()
z_values = "".join(list([str(wires[z]) for z in reversed(z_wires)]))

end_time = time.perf_counter()
print(f"Zs: {z_values}")

# not 764 : 0001011111100
# not 26546678708189 : 0110000010010011100001010110101011011111011101

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
