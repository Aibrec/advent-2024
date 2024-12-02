import re

file_path = 'input.txt'

# Open the file in read mode ('r')
with open(file_path, 'r') as file:
    safe = 0
    for line in file:
        numbers = line.split()
        previous = 0
        direction = 0
        for i in range(len(numbers)):
            if i == 0:
                previous = int(numbers[i])
                continue

            current = int(numbers[i])
            difference = current - previous

            if difference == 0:
                break

            if abs(difference) > 3:
                break

            cur_direction = difference / abs(difference)
            if i == 1:
                direction = cur_direction
            else:
                if direction != cur_direction:
                    break

            previous = current
        else:
            safe += 1

print(f"safe is {safe}")
