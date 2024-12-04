import time
from collections import defaultdict

file_path = 'input.txt'

locations = defaultdict(int)
def search_diagonal(x_unit, y_unit, x, y, word_search, line_length, num_lines):
    word = 'MAS'
    for i in range(3):
        next_x = x + i*x_unit
        next_y = y + i*y_unit
        if not((0 <= next_x < line_length) and (0 <= next_y < num_lines)):
            return
        elif word_search[next_y][next_x] != word[i]:
            return
    else:
        locations[(y+y_unit, x+x_unit)] += 1
        return

start = time.time_ns()
with open(file_path, 'r') as file:
    word_search = []
    for line in file:
        word_search.append(line.strip())

    line_length = len(word_search[0])
    num_lines = len(word_search)

    for x in range(line_length):
        for y in range(num_lines):
            if word_search[y][x] != 'M':
                continue

            search_diagonal(1, 1, x, y, word_search, line_length, num_lines)
            search_diagonal(-1, 1, x, y, word_search, line_length, num_lines)
            search_diagonal(1, -1, x, y, word_search, line_length, num_lines)
            search_diagonal(-1, -1, x, y, word_search, line_length, num_lines)

    sum = 0
    for key,value in locations.items():
        if value == 2:
            sum += 1

end = time.time_ns()
print(f"sum is {sum}")

time_in_microseconds = (end-start) / 1000
print(f"took {time_in_microseconds}μs")
