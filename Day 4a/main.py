import time
import re

file_path = 'input.txt'

def check_for_xmas(y, x, word_search, line_length, num_lines):
    sum = 0

    # Check forwards
    if x+3 < line_length and word_search[y][x:x+4] == 'XMAS':
        sum += 1

    # Check backwards
    if x >= 3 and word_search[y][x-3:x+1] == 'SAMX':
        sum += 1

    # Check up
    if y >= 3 and (word_search[y][x] + word_search[y-1][x] + word_search[y-2][x] + word_search[y-3][x]) == 'XMAS':
        sum += 1

    # Check down
    if y+3 < num_lines and (word_search[y][x] + word_search[y+1][x] + word_search[y+2][x] + word_search[y+3][x]) == 'XMAS':
        sum += 1

    # for yi in (1,-1):
    #     for xi in (1,-1):
    #         if 0 <= (x+xi*3) < line_length and 0 <= (y+yi*3) < num_lines:
    #             if (word_search[y][x] + word_search[y + yi*1][x + xi*1] + word_search[y + yi*2][x + xi*2] + word_search[y + yi*3][x + xi*3]) == 'XMAS':
    #                 sum += 1

    #
    # Check diagonal up-left
    try:
        if x >= 3 and y >= 3:
            if (word_search[y][x] + word_search[y-1][x-1] + word_search[y-2][x-2] + word_search[y-3][x-3]) == 'XMAS':
                sum += 1
    except IndexError:
        pass

    # Check diagonal up-right
    try:
        if y >= 3:
            if (word_search[y][x] + word_search[y-1][x+1] + word_search[y-2][x+2] + word_search[y-3][x+3]) == 'XMAS':
                sum += 1
    except IndexError:
        pass

    # Check diagonal down-right
    try:
        if (word_search[y][x] + word_search[y+1][x+1] + word_search[y+2][x+2] + word_search[y+3][x+3]) == 'XMAS':
            sum += 1
    except IndexError:
        pass

    # Check diagonal down-left
    try:
        if x >= 3:
            if (word_search[y][x] + word_search[y+1][x-1] + word_search[y+2][x-2] + word_search[y+3][x-3]) == 'XMAS':
                sum += 1
    except IndexError:
        pass

    return sum

start = time.time_ns()
with open(file_path, 'r') as file:

    sum = 0
    enabled = True
    word_search = []
    sum = 0
    for line in file:
        word_search.append(line.strip())

    line_length = len(word_search[0])
    num_lines = len(word_search)
    for x in range(line_length):
        for y in range(num_lines):
            if word_search[y][x] != 'X':
                continue

            sum += check_for_xmas(y, x, word_search, line_length, num_lines)

end = time.time_ns()
print(f"sum is {sum}")

time_in_microseconds = (end-start) / 1000
print(f"took {time_in_microseconds}μs")
