import time
import re

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    mul = re.compile('mul\((\d+),(\d+)\)')
    sum = 0
    for line in file:
        matches = re.findall(mul, line)
        numbers = line.split()
        for match in matches:
            result = int(match[0]) * int(match[1])
            sum += result
end = time.perf_counter()
print(f"sum is {sum}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.2f}μs")
