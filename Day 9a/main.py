import time

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    defragged = []
    fragged = None
    for line in file:
        fragged = list([int(n) for n in line.strip()])

left = 0
right = len(fragged) - 1 # TODO: Have to check it's an odd number.

if ((right % 2) + 1) == 0:
    right -= 1  # If it's even it's pointing at blank space, so go down to the file instead

left_file_count = 0
right_file_count = 100000  # Arbitrary, just has to be higher than half the total or so
right_file_remaining = 0
next_type = "File"
while right >= left:
    if next_type == "File":
        # Place the file from the left into the defragged disk
        defragged.append((left_file_count, fragged[left]))
        left_file_count += 1
        left += 1
        next_type = "Free space"
    elif next_type == "Free space":
        # Fill in the free space with a file from the right
        space_available = fragged[left]
        while space_available:
            if right_file_remaining:
                space_used = min(space_available, right_file_remaining)
                defragged.append((right_file_count, min(space_available, right_file_remaining)))
                right_file_remaining = max(0, right_file_remaining - space_used)
                space_available = max(0, space_available - space_used)
            else:
                # Get a file from the right
                right_file_remaining = fragged[right]
                right -= 2
                right_file_count += 1
        left += 1
        next_type = "File"

if right_file_remaining:
    defragged.append((right_file_count, right_file_remaining))

total_files = right_file_count-100000 + left_file_count - 1
right_file_maps = {}
for i, file in enumerate(defragged):
    if file[0] >= 100000:
        if file[0] not in right_file_maps:
            right_file_maps[file[0]] = total_files
            total_files -= 1

        val = (right_file_maps[file[0]], file[1])
        defragged[i] = val

sum = 0
position = 0
for file in defragged:
    for i in range(1,file[1]+1):
        sum += position * file[0]
        position += 1

end = time.perf_counter()
print(f"sum is {sum}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.2f}μs")
