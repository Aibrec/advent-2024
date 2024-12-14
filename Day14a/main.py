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
    robot[0] = (((robot[0][0]+robot[1][0]*steps)%space[0]), ((robot[0][1]+robot[1][1]*steps)% space[1]))

steps = 100
zones = [0,0,0,0]
middle_y = space[0] // 2
middle_x = space[1] // 2
for robot in robots:
    #robot[0] = (((robot[0][0] + robot[1][0] * 100) % space[0]), ((robot[0][1] + robot[1][1] * 100) % space[1]))
    #move_robot(robot, steps)
    y,x = robot[0]
    y = (robot[0][0] + robot[1][0] * 100) % space[0]
    x = (robot[0][1] + robot[1][1] * 100) % space[1]
    if y < middle_y and x < middle_x:
        zones[0] += 1
    elif y > middle_y and x < middle_x:
        zones[2] += 1
    elif y < middle_y and x > middle_x:
        zones[1] += 1
    elif y > middle_y and x > middle_x:
        zones[3] += 1

total = zones[0] * zones[1] * zones[2] * zones[3]

end = time.perf_counter()
print(f"sum is {total}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
