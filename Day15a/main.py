import time

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    warehouse = []
    for line in file:
        line = line.strip()
        if not line:
            break
        warehouse.append(list([char for char in line]))

    commands = ""
    for line in file:
        commands += line.strip()

robot = None
for y, line in enumerate(warehouse):
    for x, char in enumerate(line):
        if char == '@':
            robot = (y,x)
            warehouse[y][x] = '.'
            break
    else:
        continue
    break

def char_to_dir(char):
    if char == '<':
        return 0,-1
    elif char == '^':
        return -1,0
    elif char == '>':
        return 0, 1
    elif char == 'v':
        return 1,0
    else:
        raise ValueError

def add_dir(dir, coord):
    return dir[0] + coord[0], dir[1] + coord[1]

def get_coord(coord, warehouse):
    return warehouse[coord[0]][coord[1]]

def move(object, dir, warehouse):
    next_coord = add_dir(dir, object)
    char = get_coord(next_coord, warehouse)
    if char == 'O':
        # Barrel, try moving the barrel
        move(next_coord, dir, warehouse)
        char = get_coord(next_coord, warehouse)

    if char == '.':
        # Open space, move to it
        warehouse[next_coord[0]][next_coord[1]] = warehouse[object[0]][object[1]]
        warehouse[object[0]][object[1]] = '.'
        return next_coord
    elif char == '#' or char == 'O':
        # Blocked space, can't move
        return object
    else:
        raise ValueError

def print_warehouse(warehouse):
    for y, line in enumerate(warehouse):
        print("".join(line))
    print('')

for command in commands:
    dir = char_to_dir(command)
    robot = move(robot, dir, warehouse)
    #print_warehouse(warehouse)

score = 0
for y, line in enumerate(warehouse):
    for x, char in enumerate(line):
        if char == 'O':
            score += 100*y + x

end = time.perf_counter()
print(f"score is {score}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
