import time
import re

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

start = time.time_ns()
with open(file_path, 'r') as file:

    sum = 0
    enabled = True
    word_search = []
    sum = 0
    for line in file:
        word_search.append(line.strip())

    for line in word_search:
        xmas = re.findall('XMAS', line)
        samx = re.findall('SAMX', line)
        sum += (len(xmas) + len(samx))

    for x in range(len(word_search[0])):
        vertical_line = "".join([word_search[y][x] for y in range(len(word_search))])
        xmas = re.findall('XMAS', vertical_line)
        samx = re.findall('SAMX', vertical_line)
        sum += (len(xmas) + len(samx))

    line_length = len(word_search[0])
    num_lines = len(word_search)
    for x in range(line_length):
        for y in range(num_lines):
            if word_search[y][x] != 'X':
                continue

            sum += search_diagonal(1, 1, x, y, word_search, line_length, num_lines)
            sum += search_diagonal(-1, 1, x, y, word_search, line_length, num_lines)
            sum += search_diagonal(1, -1, x, y, word_search, line_length, num_lines)
            sum += search_diagonal(-1, -1, x, y, word_search, line_length, num_lines)

end = time.time_ns()
print(f"sum is {sum}")

time_in_microseconds = (end-start) / 1000
print(f"took {time_in_microseconds}μs")
