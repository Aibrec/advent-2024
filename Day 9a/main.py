import time
import llist
from llist import dllist

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    for line in file:
        input = list([int(n) for n in line.strip()])

disk = []
next_type = "file"
next_file = 0
free_space_indexes = []
file_indexes = []
for n in input:
    if next_type == "file":
        disk.append((next_file, n))
        file_indexes.append(len(disk)-1)
        next_file += 1
        next_type = "free"
    elif next_type == "free":
        if n != 0:
            disk.append([-1, n, dllist()])
            free_space_indexes.append(len(disk)-1)
        next_type = "file"

right = len(file_indexes) - 1
right_file_id = 0
right_file_remaining = 0
for left in free_space_indexes:
    file = disk[left]

    # Fill in the free space with a file from the right
    space_available = file[1]
    while space_available:
        if not right_file_remaining:
            if file_indexes[right] < left:
                break

            # Get a file from the right
            file_index = file_indexes[right]
            right_file_id = disk[file_index][0]
            right_file_remaining = disk[file_index][1]
            disk[file_index] = None
            right -= 1

        if right_file_remaining:
            space_used = min(space_available, right_file_remaining)
            file[2].append((right_file_id, space_used))
            file[1] -= space_used

            right_file_remaining = max(0, right_file_remaining - space_used)
            space_available = max(0, space_available - space_used)

if right_file_remaining:
    disk[file_indexes[right+1]] = (right_file_id, right_file_remaining)

def sum_1_to_n(n):
    return (n * (n+1)) // 2

sum = 0
position = 0
for file in disk:
    if file is None:
        break

    if file[0] != -1:
        part = file[0] * ((position*file[1]) + sum_1_to_n(file[1]-1))
        sum += part
        position += file[1]
    else:
        for inner_file in file[2]:
            part = inner_file[0] * ((position * inner_file[1]) + sum_1_to_n(inner_file[1] - 1))
            sum += part
            position += inner_file[1]
        position += file[1]

end = time.perf_counter()
print(f"sum is {sum}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.2f}μs")
