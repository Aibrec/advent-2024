import time
import re
from collections import defaultdict

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    robots = []
    pat = re.compile('p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)')
    for line in file:
        match = re.match('p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line.strip()).groups()
        coords = (int(match[1]), int(match[0]))
        velocity = (int(match[3]), int(match[2]))
        robots.append((coords, velocity))

space = (103,101)
def move_robot(robot, steps):
    position = robot[0]
    velocity = robot[1]
    absolute_position = (position[0]+velocity[0]*steps, position[1]+velocity[1]*steps)
    wrapped_position = (absolute_position[0] % space[0], absolute_position[1] % space[1])
    return wrapped_position

map = defaultdict(int)
steps = 100
for robot in robots:
    position = move_robot(robot, steps)
    map[position] += 1

middle_y = space[0] // 2
middle_x = space[1] // 2

zones = [0,0,0,0]
for coord in map.keys():
    y = coord[0]
    x = coord[1]
    if y < middle_y and x < middle_x:
        zones[0] += map[coord]
    elif y > middle_y and x < middle_x:
        zones[2] += map[coord]
    elif y < middle_y and x > middle_x:
        zones[1] += map[coord]
    elif y > middle_y and x > middle_x:
        zones[3] += map[coord]

total = zones[0] * zones[1] * zones[2] * zones[3]

end = time.perf_counter()
print(f"sum is {total}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
