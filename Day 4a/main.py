import time

file_path = 'input.txt'

def check_for_xmas(y, x, word_search):
    sum = 0

    # Check forwards
    try:
        if word_search[y][x:x+4] == 'XMAS':
            sum += 1
    except IndexError:
        pass

    # Check backwards
    if x >= 3 and word_search[y][x-3:x+1] == 'SAMX':
        sum += 1

    # Check up
    if y >= 3 and (word_search[y][x] + word_search[y-1][x] + word_search[y-2][x] + word_search[y-3][x]) == 'XMAS':
        sum += 1

    # Check down
    try:
        if (word_search[y][x] + word_search[y+1][x] + word_search[y+2][x] + word_search[y+3][x]) == 'XMAS':
            sum += 1
    except IndexError:
        pass

    # Nicer, but slower
    # for yi in (1,-1):
    #     for xi in (1,-1):
    #         if 0 <= (x+xi*3) < line_length and 0 <= (y+yi*3) < num_lines:
    #             if (word_search[y][x] + word_search[y + yi*1][x + xi*1] + word_search[y + yi*2][x + xi*2] + word_search[y + yi*3][x + xi*3]) == 'XMAS':
    #                 sum += 1

    # Check diagonal up-left
    if x >= 3 and y >= 3 and (word_search[y][x] + word_search[y-1][x-1] + word_search[y-2][x-2] + word_search[y-3][x-3]) == 'XMAS':
        sum += 1

    # Check diagonal up-right
    try:
        if y >= 3 and (word_search[y][x] + word_search[y-1][x+1] + word_search[y-2][x+2] + word_search[y-3][x+3]) == 'XMAS':
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
        if x >= 3 and (word_search[y][x] + word_search[y+1][x-1] + word_search[y+2][x-2] + word_search[y+3][x-3]) == 'XMAS':
            sum += 1
    except IndexError:
        pass

    return sum

start = time.time_ns()
with open(file_path, 'r') as file:
    word_search = []
    for line in file:
        word_search.append(line.strip())

    sum = 0
    for y, column in enumerate(word_search):
        for x, char in enumerate(column):
            if char != 'X':
                continue
            else:
                sum += check_for_xmas(y, x, word_search)

end = time.time_ns()
print(f"sum is {sum}")

time_in_microseconds = (end-start) / 1000
print(f"took {time_in_microseconds}μs")
