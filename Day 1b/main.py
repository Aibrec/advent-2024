import re

file_path = 'input.txt'

# Open the file in read mode ('r')
with open(file_path, 'r') as file:
    left_list = []
    right_dict = {}
    for line in file:
        numbers = line.split()
        left_list.append(int(numbers[0]))

        right_num = int(numbers[1])
        if right_num not in right_dict:
            right_dict[right_num] = 0
        right_dict[right_num] += 1

sum = 0
for i in range(len(left_list)):
    if left_list[i] in right_dict:
        sum += right_dict[left_list[i]] * left_list[i]

print(f"Sum is {sum}")
