import time

file_path = 'input.txt'

def check_for_mas(y, x, word_search):
    try:
        if y > 0 and x > 0:
            if {word_search[y - 1][x - 1], word_search[y + 1][x + 1]} == {'M', 'S'}:
                if {word_search[y - 1][x + 1], word_search[y + 1][x - 1]} == {'M', 'S'}:
                    return True
            return False
    except IndexError:
        return False


start = time.time_ns()
with open(file_path, 'r') as file:
    word_search = []
    for line in file:
        word_search.append(line.strip())

    sum = 0
    for x in range(len(word_search[0])):
        for y in range(len(word_search)):
            if word_search[y][x] != 'A':
                continue

            if check_for_mas(y, x, word_search):
                sum +=1

end = time.time_ns()
print(f"sum is {sum}")

time_in_microseconds = (end-start) / 1000
print(f"took {time_in_microseconds}μs")
