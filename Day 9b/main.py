import time
import bisect

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    defragged = []
    fragged = None
    for line in file:
        fragged = list([int(n) for n in line.strip()])

disk = []
next_type = "file"
next_file = 0
for n in fragged:
    if next_type == "file":
        disk.append((next_file, n))
        next_file += 1
        next_type = "free"
    elif next_type == "free":
        if n != 0:
            disk.append([-1, n, []])
        next_type = "file"

disk = list(reversed(disk))  # So we can mutate ahead instead of behind

free_spaces = {}
for i, file in enumerate(disk):
    if file[0] == -1:
        if file[1] not in free_spaces:
            free_spaces[file[1]] = []
        free_spaces[file[1]].append((i, file))

i = 0
while i < len(disk):
    file = disk[i]
    if file[0] != -1:
        size = file[1]

        largest_index = -1
        largest_index_s = -1
        for s in free_spaces.keys():
            if s < size or not free_spaces[s]:
                continue

            right_most_space = free_spaces[s][-1]
            if right_most_space[0] > largest_index:
                largest_index = right_most_space[0]
                largest_index_s = s

        if largest_index != -1:
            disk_location = largest_index

            if disk_location > i:
                disk[i] = (-1, file[1], [])  # mark the file as free space

                disk[disk_location][2].append(file)
                disk[disk_location][1] = disk[disk_location][1] - size

                free_spaces[largest_index_s].pop()
                if disk[disk_location][1] > 0:
                    bisect.insort(free_spaces[disk[disk_location][1]], (disk_location, disk[disk_location]))
    i += 1

def sum_1_to_n(n):
    return (n * (n+1)) // 2

sum = 0
position = 0
for file in reversed(disk):
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
