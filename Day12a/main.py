import time

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    farm = []
    for line in file:
        farm.append(line.strip())

def get_adjacent(coord):
    return ((coord[0]-1, coord[1]), (coord[0]+1, coord[1]), (coord[0], coord[1]-1), (coord[0], coord[1]+1))

def get_value(coord, farm):
    y,x = coord
    if y >= 0 and x >= 0:
        try:
            return farm[y][x]
        except IndexError:
            pass
    return -1

def flood_fill(starting_coord, farm):
    field = set()
    perimeter = 0
    to_expand = {starting_coord}

    field_crop = get_value(starting_coord, farm)
    while to_expand:
        coord = to_expand.pop()
        adjacent = get_adjacent(coord)
        for adj_coord in adjacent:
            adj_crop = get_value(adj_coord, farm)
            if adj_crop != field_crop:
                perimeter += 1
            elif adj_coord not in field:
                to_expand.add(adj_coord)

        field.add(coord)

    return field, perimeter

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
