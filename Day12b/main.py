import time
from collections import defaultdict

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    farm = []
    for line in file:
        farm.append(line.strip())

def dirs():
     return (-1, 0), (1, 0), (0, -1), (0, 1)

def add_dir(coord, dir):
    return (coord[0] + dir[0], coord[1] + dir[1])

def get_value(coord):
    y,x = coord
    if y >= 0 and x >= 0:
        try:
            return farm[y][x]
        except IndexError:
            pass
    return -1

def perpendicular_dirs(dir):
    if dir[0] == 1 or dir[0] == -1:
        return (0,1), (0,-1)
    else:
        return (1,0), (-1,0)

def follow_line(starting_coord, crop, edge_dir):
    line = {starting_coord}
    line_dirs = perpendicular_dirs(edge_dir)
    for dir in line_dirs:
        next_coord = starting_coord
        while True:
            next_coord = add_dir(next_coord, dir)
            next_adj_coord = add_dir(next_coord, edge_dir)
            if crop == get_value(next_coord) and crop != get_value(next_adj_coord):
                line.add(next_coord)
            else:
                break
    return line

def flood_fill(starting_coord, farm):
    field = set()
    to_expand = {starting_coord}

    edges_by_dir = defaultdict(set)

    field_crop = get_value(starting_coord)
    while to_expand:
        coord = to_expand.pop()
        for dir in dirs():
            adj_coord = add_dir(coord, dir)
            adj_crop = get_value(adj_coord)
            if adj_crop != field_crop:
                edges_by_dir[dir].add(coord)
            elif adj_coord not in field:
                to_expand.add(adj_coord)

        field.add(coord)

    lines = 0
    for dir, edges in edges_by_dir.items():
        while edges:
            edge_coord = edges.pop()
            line = follow_line(edge_coord, field_crop, dir)
            edges -= line
            lines += 1

    return field, lines

seen_coords = set()
fields = []
total = 0
for y, line in enumerate(farm):
    for x, crop in enumerate(line):
        if (y,x) not in seen_coords:
            field, perimeter = flood_fill((y,x), farm)
            seen_coords = seen_coords.union(field)
            fields.append(field)
            total += len(field) * perimeter

end = time.perf_counter()
print(f"sum is {total}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
