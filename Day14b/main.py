import time
import re

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    robots = []
    pat = re.compile('p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)')
    for line in file:
        match = re.match('p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line.strip()).groups()
        coords = (int(match[1]), int(match[0]))
        velocity = (int(match[3]), int(match[2]))
        robots.append([coords, velocity])

space = (103,101)
def move_robot(robot, steps):
    position = robot[0]
    velocity = robot[1]
    absolute_position = (position[0]+velocity[0]*steps, position[1]+velocity[1]*steps)
    wrapped_position = (absolute_position[0] % space[0], absolute_position[1] % space[1])
    return wrapped_position

def dirs():
    return (-1, 0), (1, 0), (0, -1), (0, 1)

def all_dirs_from(coord):
    for dir in dirs():
        yield (coord[0]+dir[0], coord[1]+dir[1])

def print_map(robots, step_count):
    print(f'\nAfter Step {step_count}')
    map = []
    for y in range(space[0]):
        map.append([" "] * space[1])

    for robot in robots:
        map[robot[0][0]][robot[0][1]] = '*'

    for line in map:
        print("".join(line))

map = []
for y in range(space[0]):
    map.append([0] * space[1])

step_count = 0
while True:
    step_count += 1
    robot_locations = set()

    for i, robot in enumerate(robots):
        position = move_robot(robot, 1)
        robot[0] = position
        robot_locations.add(position)

    # density = 0
    # for robot_coord in robot_locations:
    #     for adj in all_dirs_from(robot_coord):
    #         if adj in robot_locations:
    #             density += 1
    # if density > 300:
    #     print(f'try {step_count}')

    if len(robot_locations) == len(robots):
        #print(f'All unique at {step_count}')
        #print_map(robots, step_count)
        break

end = time.perf_counter()
print(f"tree at {step_count}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
