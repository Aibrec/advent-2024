import time
import functools
from collections import defaultdict

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    stones = defaultdict(int)
    for line in file:
        nums = list(int(n) for n in line.strip().split())
        for num in nums:
            stones[num] += 1

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

def increment_all_stones(stones, new_stones):
    for stone, count in stones.items():
        for new_stone in increment_stone(stone):
            new_stones[new_stone] += count
        stones[stone] = 0

new_stones = defaultdict(int)
for i in range(75):
    increment_all_stones(stones, new_stones)
    stones,new_stones = new_stones, stones

total_stones = sum(stones.values())

end = time.perf_counter()
print(f"sum is {total_stones}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
