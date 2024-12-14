import time
import re

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    robots = []
    pat = re.compile('p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)')
    for line in file:
        match = re.match('p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line.strip()).groups()
        coords = [int(match[1]), int(match[0])]
        velocity = (int(match[3]), int(match[2]))
        robots.append([coords, velocity])

space = (103,101)
def move_robot(robot, steps):
    robot[0] = (((robot[0][0]+robot[1][0]*steps)%space[0]), ((robot[0][1]+robot[1][1]*steps)% space[1]))

def dirs():
    return (-1, 0), (1, 0), (0, -1), (0, 1)

# def all_dirs_from(coord):
#     for dir in dirs():
#         yield (coord[0]+dir[0], coord[1]+dir[1])

def print_map(robots, step_count):
    print(f'\nAfter Step {step_count}')
    map = []
    for y in range(space[0]):
        map.append([" "] * space[1])

    for robot in robots:
        map[robot[0][0]][robot[0][1]] = '*'

    for line in map:
        print("".join(line))

step_count = 0
robot_locations = set()
while True:
    step_count += 1
    all_unique_locations = True
    for i, robot in enumerate(robots):
        robot[0] = (((robot[0][0] + robot[1][0]) % space[0]), ((robot[0][1] + robot[1][1]) % space[1]))
        if all_unique_locations and robot[0] not in robot_locations:
            robot_locations.add(robot[0])
        else:
            all_unique_locations = False

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

    robot_locations.clear()

end = time.perf_counter()
print(f"tree at {step_count}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
