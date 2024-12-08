import time

file_path = 'input.txt'

start = time.time_ns()
with open(file_path, 'r') as file:
    map = []
    letter_maps = {}
    for line in file:
        map.append(line.strip())

        for x, char in enumerate(map[-1]):
            if char == '.':
                continue

            if char not in letter_maps:
                letter_maps[char] = set()

            letter_maps[char].add((len(map)-1, x))

antinodes = set()
for char, points in letter_maps.items():
    for a in points:
        for b in points:
            if a == b:
                continue

            difference = (a[0]-b[0], a[1]-b[1])
            antinode = (a[0]+difference[0], a[1]+difference[1])
            if 0 <= antinode[0] < len(map) and 0 <= antinode[1] < len(map):
                antinodes.add(antinode)

end = time.time_ns()
print(f"sum is {len(antinodes)}")

time_in_microseconds = (end-start) / 1000
print(f"took {time_in_microseconds}μs")
