import time

file_path = 'input.txt'

start = time.time_ns()
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

end = time.time_ns()
print(f"Sum is {sum}")

time_in_microseconds = (end-start) / 1000
print(f"took {time_in_microseconds}μs")