import time
import networkx as nx

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

        # Do them based on distance from A on the directional pad. So <, then V, then ^, then >, where possible
        # It's shorter to do all the moves in one dimension first.
        # We need to avoid moving over a None square
        if cursor[0] == 3 and target[1] == 0:
            numeric_moves.extend(vertical_moves)
            numeric_moves.extend(horizontal_moves)
        else:
            if horizontal_moves and horizontal_moves[0] == '<':
                numeric_moves.extend(horizontal_moves)
                numeric_moves.extend(vertical_moves)
            elif vertical_moves and vertical_moves[0] == 'v':
                numeric_moves.extend(vertical_moves)
                numeric_moves.extend(horizontal_moves)
            else:
                numeric_moves.extend(horizontal_moves)
                numeric_moves.extend(vertical_moves)
        numeric_moves.append('A')
        cursor = target

    #print(f'Numeric pad moves: {"".join(numeric_moves)}')
    return "".join(numeric_moves)

def solve_directional_code(code):
    directional_moves = []
    cursor = (0, 2)  # Starts at a
    for char in code:
        target = directional_keyboard_locations[char]
        required_moves = (target[0] - cursor[0], target[1] - cursor[1])

        vertical_moves = (['v'] if required_moves[0] > 0 else ['^']) * abs(required_moves[0])
        horizontal_moves = (['>'] if required_moves[1] > 0 else ['<']) * abs(required_moves[1])

        # Do them based on distance from a. So <, then V, then ^, then >, where possible
        # If there are '<' required do them first
        if required_moves[1] < 0:
            if target == (1, 0):
                directional_moves.extend(vertical_moves)
                directional_moves.extend(horizontal_moves)

            else:
                directional_moves.extend(horizontal_moves)
                directional_moves.extend(vertical_moves)
        else:
            # It's shorter to do all the moves in one dimension first.
            # We need to avoid moving over a None square
            # We default to moving y first unless None is in the way. It only blocks moves when the cursor is on (1,0)
            if cursor == (1, 0):
                directional_moves.extend(horizontal_moves)
                directional_moves.extend(vertical_moves)
            else:
                directional_moves.extend(vertical_moves)
                directional_moves.extend(horizontal_moves)

        # Default to horizontal firsts
        # Works unless we're moving to (1,0)
        # if target == (1, 0):
        #     directional_moves.extend(vertical_moves)
        #     directional_moves.extend(horizontal_moves)
        #
        # else:
        #     directional_moves.extend(horizontal_moves)
        #     directional_moves.extend(vertical_moves)

        directional_moves.append('A')
        cursor = target

    #print(f'Directional pad moves: {"".join(directional_moves)}')
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

# how_to_type_theirs = solve_directional_code('v<<AA>^AA>A')
# len_theirs = len(how_to_type_theirs)
# how_to_type_ours = solve_directional_code('<AAv<AA>>^A')
# len_ours = len(how_to_type_ours)

score = 0
for code in codes:
    numeric_code = solve_numeric_code(code)
    first_directional_code = solve_directional_code(numeric_code)
    second_directional_code = solve_directional_code(first_directional_code)

    # correct_answer = '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'
    # reversed_first = reverse_directional_code(correct_answer)
    # reversed_numeric = reverse_directional_code(reversed_first)
    # reversed_original_code = reverse_numeric_code(reversed_numeric)

    #print(f"second input: {"".join(second_directional_code)}")
    code_number = int(code[:-1])
    #print(f"{code}: {code_number} {len(second_directional_code)} {code_number * len(second_directional_code)}")
    score += code_number * len(second_directional_code)

total_end_time = time.perf_counter()
print(f"score is {score}")

time_in_microseconds = (total_end_time-total_start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
