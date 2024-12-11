import time
import functools
from collections import defaultdict

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    stones = []
    for line in file:
        stones = list(int(n) for n in line.strip().split())

@functools.cache
def increment_stone(stone):
    if stone == 0:
        return [1]
    elif (len(str_stone := str(stone))) % 2 == 0:
        left = str_stone[:len(str_stone)//2]
        right= str_stone[len(str_stone)//2:]
        return [int(left), int(right)]
    else:
        return [stone*2024]

@functools.cache
def increment_stone_n_count(stone, n):
    next_stones = increment_stone(stone)
    n = n-1
    if n == 0:
        return len(next_stones)
    else:
        num_stones = 0
        for next_stone in next_stones:
            num_stones += increment_stone_n_count(next_stone, n)
        return num_stones

sum = 0
for stone in stones:
    sum += increment_stone_n_count(stone, 25)

end = time.perf_counter()
print(f"sum is {sum}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
