import time

file_path = 'input.txt'

start = time.time_ns()
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

end = time.time_ns()
print(f"Sum is {sum}")

time_in_microseconds = (end-start) / 1000
print(f"took {time_in_microseconds}μs")