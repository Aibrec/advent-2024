import time
import regex as re

file_path = 'input.txt'

def search_diagonal(x_unit, y_unit, x, y, word_search, line_length, num_lines):
    word = 'XMAS'
    for i in range(4):
        next_x = x + i*x_unit
        next_y = y + i*y_unit
        if not((0 <= next_x < line_length) and (0 <= next_y < num_lines)):
            return 0
        elif word_search[next_y][next_x] != word[i]:
            return 0
    else:
        return 1

def search_with_gaps(word_search, gap_size):
    space_pattern = f".{{{gap_size}}}"
    pattern = f"X{space_pattern}M{space_pattern}A{space_pattern}S"
    matches = re.findall(pattern,word_search, overlapped=True)

    reverse_pattern = f"S{space_pattern}A{space_pattern}M{space_pattern}X"
    matches.extend(re.findall(reverse_pattern,word_search, overlapped=True))

    sum = 0
    for match in matches:
        if match.count('|') == 3:
            sum += 1
    return sum

def search(word_search):
    matches = re.findall("XMAS",word_search)
    matches.extend(re.findall("SAMX",word_search))
    return len(matches)

start = time.time_ns()
with open(file_path, 'r') as file:

    sum = 0
    enabled = True
    word_search = ""
    sum = 0
    for line in file:
        line_length = len(line.strip()) + 1
        word_search += f"{line.strip()}|"

    horizontal = search(word_search)
    vertical = search_with_gaps(word_search, line_length - 1)
    diagonal_right = search_with_gaps(word_search, line_length)
    diagonal_left = search_with_gaps(word_search, line_length - 2)
    sum += horizontal + vertical + diagonal_right + diagonal_left

end = time.time_ns()
print(f"sum is {sum}")

time_in_microseconds = (end-start) / 1000
print(f"took {time_in_microseconds}μs")
