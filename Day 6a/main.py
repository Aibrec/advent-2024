import time

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    map = []
    for line in file:
        map.append(list([c for c in line.strip()]))

for y, line in enumerate(map):
    for x, char in enumerate(line):
        if char == '^':
            start_coord = (y,x)

def turn_right(dir):
    if dir == (-1,0):
        return (0,1)
    elif dir == (0,1):
        return (1,0)
    elif dir == (1,0):
        return (0,-1)
    elif dir == (0,-1):
        return (-1,0)

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

start_dir = (-1, 0)
squares_visited = walk(start_coord, start_dir, map)
sum = len(squares_visited)

end = time.perf_counter()
print(f"sum is {sum}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.2f}μs")
