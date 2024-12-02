import time

file_path = 'input.txt'

def difference_list(num_list):
    diff_list = []
    previous = None
    for i in range(len(num_list)):
        current = int(num_list[i])
        if i != 0:
            diff_list.append(current - previous)
        previous = current
    return diff_list

def find_first_unsafe(diff_list, numbers):
    for i, num in enumerate(diff_list):
        if num == 0:
            return i

    direction = 0
    for i, num in enumerate(diff_list):
        cur_direction = num/abs(num)
        if i == 0:
            direction = cur_direction
        elif direction != cur_direction:
            return i

    for i, num in enumerate(diff_list):
        if abs(num) > 3:
            return i

    return -1

def try_variants(i, numbers):
    try_without = [i]
    if i != 0:
        try_without.append(i - 1)

    if (i+1) < len(numbers):
        try_without.append(i + 1)

    for t in try_without:
        test_list = numbers.copy()
        del test_list[t]

        diff_list = difference_list(test_list)

        if find_first_unsafe(diff_list, test_list) == -1:
            return True

    return False

start = time.time_ns()
# Open the file in read mode ('r')
with open(file_path, 'r') as file:
    safe = 0
    for line in file:
        numbers = line.split()
        diff_list = difference_list(line.split())
        if (fail_index := find_first_unsafe(diff_list, numbers)) == -1 or try_variants(fail_index, numbers):
            safe += 1
end = time.time_ns()
print(f"safe is {safe}")

time_in_microseconds = (end-start) / 1000
print(f"took {time_in_microseconds}μs")
