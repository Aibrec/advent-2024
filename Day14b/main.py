import time
import re
import numpy as np
from jax import jit

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    robots = [[], [], [], []]
    for line in file:
        match = re.match('p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line.strip()).groups()
        robots[0].append(int(match[1]))
        robots[1].append(int(match[0]))
        robots[2].append(int(match[3]))
        robots[3].append(int(match[2]))

for i in range(4):
    robots[i] = np.array(robots[i], np.int64)

def print_map(robots, step_count):
    print(f'\nAfter Step {step_count}')
    map = []
    for y in range(space[0]):
        map.append(["."] * space[1])

    for i in range(len(robots[0])):
        map[robots[0][i]][robots[1][i]] = '*'

    for line in map:
        print("".join(line))

def find_tree(robots, space):
    step_count = 0
    while True:
        step_count += 1

        # Add velocities and limit to map
        robots[0] += robots[2]
        robots[0] %= space[0]

        robots[1] += robots[3]
        robots[1] %= space[1]

        # Look for a busy vertical and horizontal line at the same time
        if np.bincount(robots[0]).max() > 20 and np.bincount(robots[1]).max() > 20:
            return step_count

space = (103,101)
#space = (7,11)
step_count = find_tree(robots, space)

end = time.perf_counter()
print_map(robots, step_count)
print(f"tree at {step_count}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
