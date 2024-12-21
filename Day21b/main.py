import time
import functools
from collections import defaultdict
import re

file_path = 'input.txt'

total_start_time = time.perf_counter()
with open(file_path, 'r') as file:
    codes = []
    for line in file:
        line = line.strip()
        codes.append(line)

numeric_keyboard = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [None, '0', 'A'],
]

numeric_keyboard_locations = {}
for y, line in enumerate(numeric_keyboard):
    for x, char in enumerate(line):
        if char is not None:
            numeric_keyboard_locations[char] = (y,x)

directional_keyboard = [
    [None, '^', 'A'],
    ['<', 'v', '>'],
]

directional_keyboard_locations = {}
for y, line in enumerate(directional_keyboard):
    for x, char in enumerate(line):
        if char is not None:
            directional_keyboard_locations[char] = (y,x)

def solve_numeric_code(code):
    # First map it to the numeric keyboard
    numeric_moves = []
    cursor = (3, 2)  # Starts at a
    for char in code:
        target = numeric_keyboard_locations[char]
        required_moves = (target[0] - cursor[0], target[1] - cursor[1])

        vertical_moves = (['v'] if required_moves[0] > 0 else ['^']) * abs(required_moves[0])
        horizontal_moves = (['>'] if required_moves[1] > 0 else ['<']) * abs(required_moves[1])

        # Do them based on distance from A on the directional pad. So <, then v, then ^, then >, where possible
        # It's shorter to do all the moves in one dimension first.
        # We need to avoid moving over a None square
        if cursor[0] == 3 and target[1] == 0:
            numeric_moves.extend(vertical_moves)
            numeric_moves.extend(horizontal_moves)
        elif horizontal_moves and horizontal_moves[0] == '<':
            numeric_moves.extend(horizontal_moves)
            numeric_moves.extend(vertical_moves)
        else:
            numeric_moves.extend(vertical_moves)
            numeric_moves.extend(horizontal_moves)
        numeric_moves.append('A')
        cursor = target

    #print(f'Numeric pad moves: {"".join(numeric_moves)}')
    return "".join(numeric_moves)

@functools.cache
def solve_directional_code(code):
    directional_moves = []
    cursor = (0, 2)  # Starts at a
    for char in code:
        target = directional_keyboard_locations[char]
        required_moves = (target[0] - cursor[0], target[1] - cursor[1])

        vertical_moves = (['v'] if required_moves[0] > 0 else ['^']) * abs(required_moves[0])
        horizontal_moves = (['>'] if required_moves[1] > 0 else ['<']) * abs(required_moves[1])

        # Do them based on distance from A on the directional pad. So <, then v, then ^, then >, where possible
        if target == (1, 0):
            directional_moves.extend(vertical_moves)
            directional_moves.extend(horizontal_moves)
        elif cursor == (1, 0) or (horizontal_moves and horizontal_moves[0] == '<'):
            directional_moves.extend(horizontal_moves)
            directional_moves.extend(vertical_moves)
        else:
            directional_moves.extend(vertical_moves)
            directional_moves.extend(horizontal_moves)

        directional_moves.append('A')
        cursor = target

    return "".join(directional_moves)


def reverse_numeric_code(directions):
    return reverse_directions(directions, (3, 2) , numeric_keyboard)

def reverse_directional_code(directions):
    return reverse_directions(directions, (0,2), directional_keyboard)

def reverse_directions(directions, start, map):
    characters_typed = []
    cursor = [start[0], start[1]]
    for char in directions:
        match char:
            case '^':
                cursor[0] -= 1
            case 'v':
                cursor[0] += 1
            case '<':
                cursor[1] -= 1
            case '>':
                cursor[1] += 1
            case 'A':
                characters_typed.append(map[cursor[0]][cursor[1]])
    return "".join(characters_typed)

score = 0
for code in codes:
    directions = solve_numeric_code(code)

    #chunks = re.match('^([<^v>]+A+)*$', directions)
    chunks = re.findall('([<^v>]+A+)', directions)
    code_parts = defaultdict(int)
    for chunk in chunks:
        if chunk:
            code_parts[chunk] += 1

    for n in range(25):
        next_parts = defaultdict(int)
        for part, num in code_parts.items():
            if part and num > 0:
                directions_for_part = solve_directional_code(part)
                directions_for_part_chunks = re.findall('([<^v>]+A+)', directions_for_part)
                for chunk in directions_for_part_chunks:
                    if chunk:
                        next_parts[chunk] += num
        code_parts = next_parts

    length = 0
    for part, num in code_parts.items():
        if num > 0:
            length += len(part) * num

    code_number = int(code[:-1])
    #print(f"{code}: {code_number} {length} {code_number * length}")
    score += code_number * length

total_end_time = time.perf_counter()
print(f"score is {score}")

time_in_microseconds = (total_end_time-total_start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
