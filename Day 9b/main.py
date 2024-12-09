import time

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
i = 0
while i < len(disk):
    file = disk[i]
    if file[0] != -1:
        size = file[1]
        for r in reversed(range(i+1, len(disk))):
            r_file = disk[r]
            if r_file[0] == -1 and r_file[1] >= size:
                disk[i] = (-1, file[1], [])  # mark the file as free space
                temp_of_free_space = disk[r]
                disk[r][2].append(file)
                disk[r][1] = disk[r][1] - size
                break
    i += 1

sum = 0
position = 0
disk = list(reversed(disk))
for file in disk:
    if file[0] != -1:
        for i in range(1,file[1]+1):
            if file[0] > 0:
                sum += position * file[0]
            position += 1
    else:
        for inner_file in file[2]:
            for r in range(1, inner_file[1] + 1):
                if inner_file[0] > 0:
                    sum += position * inner_file[0]
                position += 1
        position += file[1]


end = time.perf_counter()
print(f"sum is {sum}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.2f}μs")
