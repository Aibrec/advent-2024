import time

file_path = 'input.txt'

start = time.perf_counter()
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

def next_blockage(coord, dir, blockages):
    if dir[0] != 0:
        i = 1
        z = 0
    else:
        i = 0
        z = 1

    if dir[z] > 0:
        stop = next((block for block in blockages[i][coord[i]] if block[z] > coord[z]), None)
    else: # dir[i] < 0
        stop = next((block for block in blockages[i][coord[i]][::-1] if block[z] < coord[z]), None)

    return stop

def walk(coord, dir, map):
    squares_visited = {coord}

    try:
        while True:
            if coord[0]+dir[0] < 0 or coord[1]+dir[1] < 0:
                break

            next_coord = (coord[0]+dir[0], coord[1]+dir[1])
            if map[next_coord[0]][next_coord[1]] != '#':
                coord = next_coord
                squares_visited.add(coord)
            else:
                dir = turn_right(dir)
    except IndexError:
        # Walked off the map, done
        pass

    return squares_visited

def detect_loop(coord, dir, blockages):
    loop_detector = {coord, dir}
    while True:
        block = next_blockage(coord, dir, blockages)
        if not block:
            return False # No loop found

        coord = (block[0] - dir[0], block[1] - dir[1])
        dir = turn_right(dir)

        if (coord, dir) in loop_detector:
            return True # Loop found
        else:
            loop_detector.add((coord, dir))

start_dir = (-1, 0)
squares_visited = walk(start_coord, start_dir, map)
blockages = (blockages_by_y, blockages_by_x)
loops_caused = 0
for i, square in enumerate(squares_visited):
    if square == start_coord:
        continue

    before_y = blockages[0][square[0]].copy()
    before_x = blockages[1][square[1]].copy()

    blockages[0][square[0]].append(square)
    blockages[0][square[0]].sort()
    blockages[1][square[1]].append(square)
    blockages[1][square[1]].sort()

    has_loop = detect_loop(start_coord, start_dir, blockages)
    if has_loop:
        loops_caused += 1

    blockages[0][square[0]] = before_y
    blockages[1][square[1]] = before_x

end = time.perf_counter()
print(f"sum is {loops_caused}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.2f}μs")
