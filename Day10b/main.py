import time
from collections import defaultdict

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    map = []
    for line in file:
        map.append(list([int(n) for n in line.strip()]))

zeros = defaultdict(int)
for y, line in enumerate(map):
    for x, char in enumerate(line):
        if char == 0:
            zeros[(y,x)] += 1

def get_adjacent(coords):
    return [(coords[0]-1, coords[1]), (coords[0]+1, coords[1]), (coords[0], coords[1]-1), (coords[0], coords[1]+1)]

def coords_that_match(map, coords, value):
    matching = []
    for y, x in coords:
        if y >= 0 and x >= 0:
            try:
                val = map[y][x]
                if int(val) == value:
                    matching.append((y,x))
            except IndexError:
                continue
    return matching

current = zeros
next = defaultdict(int)
for i in range(1,10):
    for coord, paths in current.items():
        adjacent = get_adjacent(coord)
        matching = coords_that_match(map, adjacent, i)
        for coord in matching:
            next[coord] += paths
    current = next
    next = defaultdict(int)

sum = 0
for coord, paths in current.items():
    sum += paths

end = time.perf_counter()
print(f"sum is {sum}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.2f}μs")
