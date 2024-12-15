import time
import re
import numpy as np
from sympy.ntheory.modular import crt

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

def step_n(robots, n):
    # Add velocities and limit to map
    robots[0] += robots[2] * n
    robots[0] %= space[0]

    robots[1] += robots[3] * n
    robots[1] %= space[1]

def find_clustered_step(positions, velocities, space):
    positions = np.copy(positions)
    min_non_zero_bin = space
    step_for_min = -1

    for i in range(100):
        positions += velocities
        positions %= space

        non_zero_bins = np.count_nonzero(np.bincount(positions))
        if non_zero_bins < min_non_zero_bin:
            min_non_zero_bin = non_zero_bins
            step_for_min = i+1

    return step_for_min

space = (103,101)
y_clustered_step = find_clustered_step(robots[0], robots[2], space[0])
x_clustered_step = find_clustered_step(robots[1], robots[3], space[1])

# So we've got MinY = Y_Clustered_Step % space[0] and similar for X
# Can rearrange for step_count = MinY % space[0] and similar for X
# That's enough to use chinese remainder theorem to solve for a step where step_count satisfies the y and x
tree_count, _ = crt([space[0], space[1]], [y_clustered_step, x_clustered_step])

end = time.perf_counter()
step_n(robots, tree_count)
print_map(robots, tree_count)
print(f"tree at {tree_count}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
