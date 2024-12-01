import re

file_path = 'input.txt'

# Open the file in read mode ('r')
with open(file_path, 'r') as file:
    left_list = []
    right_list = []
    for line in file:
        numbers = line.split()
        left_list.append(int(numbers[0]))
        right_list.append(int(numbers[1]))

left_list.sort()
right_list.sort()
sum = 0
for i in range(len(left_list)):
    distance = abs(left_list[i] - right_list[i])
    sum += distance

print(f"Sum is {sum}")
