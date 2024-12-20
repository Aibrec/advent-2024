import time

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    warehouse = []
    for line in file:
        line = line.strip()
        if not line:
            break

        line = line.replace('#', '##')
        line = line.replace('O', '[]')
        line = line.replace('.', '..')
        line = line.replace('@', '@.')
        warehouse.append(list([char for char in line]))

    commands = ""
    for line in file:
        commands += line.strip()

def print_warehouse(warehouse):
    for y, line in enumerate(warehouse):
        print("".join(line))
    print('')

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

def move_robot(robot, dir, warehouse):
    next_coord = (dir[0]+robot[0], dir[1]+robot[1])
    char =  warehouse[next_coord[0]][next_coord[1]]
    match char:
        case '.':
            # Open space, move to it
            #warehouse[next_coord[0]][next_coord[1]] = warehouse[robot[0]][robot[1]]
            #warehouse[robot[0]][robot[1]] = '.'
            return next_coord
        case '[' | ']':
            if not move_barrel(next_coord, char, dir, warehouse):
                return robot
            else:
                #warehouse[next_coord[0]][next_coord[1]] = warehouse[robot[0]][robot[1]]
                #warehouse[robot[0]][robot[1]] = '.'
                return next_coord
        case '#':
            # Blocked
            return robot
        case _:
            raise ValueError

def move_barrel(barrel, barrel_char, dir, warehouse):
    to_move = {barrel, (barrel[0], barrel[1]+1) if barrel_char == '[' else (barrel[0], barrel[1]-1)}
    moves = {}
    cords_moving = set()
    while to_move:
        coord = to_move.pop()
        if coord not in cords_moving:
            next_coord = (dir[0]+coord[0], dir[1]+coord[1])
            char = warehouse[next_coord[0]][next_coord[1]]
            match char:
                case ']':
                    left = (next_coord[0], next_coord[1] - 1)
                    right = next_coord
                    if dir[0] != 0:
                        # Pushing up or down
                        to_move.add(left)
                        to_move.add(right)
                    elif dir == (0,-1):
                        moves[left] = ']'
                        to_move.add(left)
                case '[':
                    left = next_coord
                    right = (next_coord[0], next_coord[1] + 1)
                    if dir[0] != 0:
                        # Pushing up or down
                        to_move.add(left)
                        to_move.add(right)
                    elif dir == (0,1):
                        moves[right] = '['
                        to_move.add(right)
                case '#':
                    # Blocked space, can't move
                    return False

            moves[next_coord] = warehouse[coord[0]][coord[1]]
            cords_moving.add(coord)

    # Everything can be moved, so move it all
    for coord, char in moves.items():
        warehouse[coord[0]][coord[1]] = char

    # Set any coord that moved but wasn't filled to empty
    for coord in cords_moving:
        if coord not in moves:
            warehouse[coord[0]][coord[1]] = '.'

    return True

#print_warehouse(warehouse)
for command in commands:
    match command:
        case '<':
            dir = (0, -1)
        case '^':
            dir = (-1, 0)
        case '>':
            dir = (0, 1)
        case 'v':
            dir = (1, 0)
    robot = move_robot(robot, dir, warehouse)

    #print(f'command: {command}')
    #print_warehouse(warehouse)

score = 0
for y, line in enumerate(warehouse):
    for x, char in enumerate(line):
        if char == '[':
            score += 100*y + x

end = time.perf_counter()
print_warehouse(warehouse)
print(f"score is {score}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
