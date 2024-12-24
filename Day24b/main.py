import time
import networkx as nx
import matplotlib
import matplotlib.pyplot
from networkx.drawing import spring_layout
import functools

file_path = 'input.txt'

start_time = time.perf_counter()
adder = nx.Graph()
with open(file_path, 'r') as file:
    changes_from_input = {
        'z09': 'gbf',
        'gbf': 'z09',
        'z05': 'hdt',
        'hdt': 'z05',
        'z30': 'nbf',
        'nbf': 'z30',
        'jgt': 'mht',
        'mht': 'jgt',
    }

    print(f"Swapped: {",".join(sorted(changes_from_input.keys()))}")

    wires = {}
    for line in file:
        if line == '\n':
            break

        (wire, value) = line.strip().split(': ')
        wires[wire] = int(value)

        #adder.add_node(wire)

    operations = []

    operation_by_output = {}
    for line in file:
        (operation, output) = line.strip().split(' -> ')
        (left, op, right) = operation.split(' ')

        if output in changes_from_input:
            print(f"Swapped {output} for {changes_from_input[output]} in {line.strip()}")
            output = changes_from_input[output]

        sorted_inputs = sorted([left, right])

        operations.append((sorted_inputs[0], sorted_inputs[1], op, output))
        operation_by_output[output] = (sorted_inputs[0], sorted_inputs[1], op, output)

        # node_name = f"{op} {len(operations)}"
        # adder.add_node(node_name)
        # adder.add_edge(left, node_name)
        # adder.add_edge(right, node_name)
        # adder.add_edge(output, node_name)

def attempt_addition(operations, wires):
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
    return z_values

# for x in range(100):
#     for y in range(100):
#         binary_x = bin(x)[2:].zfill(45)
#         binary_y = bin(y)[2:].zfill(45)
#
#         wires = {}
#         for i in range(1,46):
#             wires[f'x{str(i-1).zfill(2)}'] = int(binary_x[-1*i])
#             wires[f'y{str(i-1).zfill(2)}'] = int(binary_y[-1*i])
#
#         binary_z = attempt_addition(operations.copy(), wires)
#         decimal_z = int(binary_z, 2)
#
#         if x+y != decimal_z:
#             print(f'Mismatch: {x}+{y} = {decimal_z}\n\t {binary_x}\n\t {binary_y}\n\t{binary_z}')
#             print('pause')

logic_names = {}
@functools.cache
def build_up_logic(wire):
    (left, right, op, output) = operation_by_output[wire]
    #logic = f"{wire}:("
    if left[0] in ('x', 'y'):
        left_logic = left
    else:
        left_logic = build_up_logic(left)

    if right[0] in ('x', 'y'):
        right_logic = right
    else:
        right_logic = build_up_logic(right)

    if len(left_logic) < len(right_logic):
        logic = f"({left_logic} {op} {right_logic})"
    else:
        logic = f"({right_logic} {op} {left_logic})"

    # if logic not in logic_names:
    #     logic_names[logic] = wire
    # else:
    #     logic = logic_names[logic]

    #logic = f"{wire}:{logic}"

    return logic

def padded_y(y):
    return f'y{str(y).zfill(2)}'

def padded_x(x):
    return f'x{str(x).zfill(2)}'

previous_length = 0
for i in range(46):
    logic = build_up_logic(f"z{str(i).zfill(2)}")
    current_length = len(logic)
    print(f"{i}: {logic}") #{len(logic)}: {current_length-previous_length}
    previous_length = current_length

    if i > 2 and i < 45:
        logic = logic.replace('(', '')
        logic = logic.replace(')', '')
        logic_list = list(logic.split(' '))
        base = 4
        for q in reversed(range(1,i)):
            next_part = logic_list[base:base+8]
            expected = [padded_y(q), "AND", padded_x(q), "OR", padded_y(q), "XOR", padded_x(q), "AND"]
            if next_part != expected:
                print('Found a broken point!')
                print(f'Expected: {expected}')
                print(f'Actual  : {next_part}')
            base = base + 8

# fig = matplotlib.pyplot.figure(figsize=(100,200))
# #nx.draw(adder, with_labels=True, pos=nx.spring_layout(adder, k=1), ax=fig.add_subplot())
# nx.draw(adder, with_labels=True, pos=nx.planar_layout(adder), ax=fig.add_subplot())
# matplotlib.use('Agg')
# fig.savefig("graph.png")

end_time = time.perf_counter()
# print(f"Zs: {z_values}")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
