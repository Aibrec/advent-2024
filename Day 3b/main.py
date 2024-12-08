import time
import re

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    mul = re.compile('((mul)\((\d+),(\d+)\))|(do\(\))|(don\'t\(\))')
    sum = 0
    enabled = True
    for line in file:
        matches = re.findall(mul, line)
        numbers = line.split()
        for match in matches:
            if match[1] == 'mul':
                if enabled:
                    result = int(match[2]) * int(match[3])
                    sum += result
            elif match[5] == 'don\'t()':
                enabled = False
            elif match[4] == 'do()':
                enabled = True

end = time.perf_counter()
print(f"sum is {sum}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.2f}μs")
