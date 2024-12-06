import time
import copy

file_path = 'input.txt'

start = time.time_ns()
with open(file_path, 'r') as file:
    map = []
    for line in file:
        map.append(list([c for c in line.strip()]))

blockages_by_y = []
blockages_by_x = list([[] for i in range(len(map[0]))])
for y, line in enumerate(map):
    blockages_by_y.append([])
    for x, char in enumerate(line):
        if char == '^':
            start_coord = (y,x)
            map[y][x] = '.'
        elif char == '#':
            blockages_by_y[y].append((y, x))
            blockages_by_x[x].append((y, x))

def turn_right(dir):
    if dir == (-1,0):
        return (0,1)
    elif dir == (0,1):
        return (1,0)
    elif dir == (1,0):
        return (0,-1)
    elif dir == (0,-1):
        return (-1,0)

def dir_to_char(dir):
    if dir == (-1,0):
        return '^'
    elif dir == (0,1):
        return '>'
    elif dir == (1,0):
        return 'v'
    elif dir == (0,-1):
        return '<'

def next_blockage(coord, dir, blockages)
    if dir[0] != 0:
        i = 0
    else:
        i = 1

    if dir[i] > 0:
        for block in blockages[i]:
            if block[i] > coord[i]:
                stop = block[i]
                break
        else:
            # off edge of map
            return None
    else: # dir[i] < 0
        for block in blockages[i]:
            if block[i] > coord[i]:
                stop = block[i]
                break
        else:
            # off edge of map
            return None

def walk(coord, dir, map):
    squares_visited = {coord}
    loop_detector = {coord, dir}
    try:
        while True:
            if coord[0]+dir[0] < 0 or coord[1]+dir[1] < 0:
                break

            next_coord = (coord[0]+dir[0], coord[1]+dir[1])
            if map[next_coord[0]][next_coord[1]] != '#':
                coord = next_coord
                squares_visited.add(coord)

                if (coord, dir) in loop_detector:
                    return squares_visited, False
                else:
                    loop_detector.add((coord, dir))

            else:
                dir = turn_right(dir)
    except IndexError:
        # Walked off the map, done
        pass

    return squares_visited, True

start_dir = (-1, 0)
squares_visited, no_loop = walk(start_coord, start_dir, map)

loops_caused = 0
for i, square in enumerate(squares_visited):
    if square == start_coord:
        continue

    obstructed_map = copy.deepcopy(map)
    obstructed_map[square[0]][square[1]] = '#'
    _, no_loop = walk(start_coord, start_dir, obstructed_map)
    if not no_loop:
        loops_caused += 1

end = time.time_ns()
print(f"sum is {loops_caused}")

time_in_microseconds = (end-start) / 1000
print(f"took {time_in_microseconds}μs")
