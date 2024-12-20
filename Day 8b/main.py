import time

file_path = 'input.txt'

start = time.perf_counter()
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
            antinode = a
            while 0 <= antinode[0] < len(map) and 0 <= antinode[1] < len(map):
                antinodes.add(antinode)
                antinode = (antinode[0]+difference[0], antinode[1]+difference[1])


end = time.perf_counter()
print(f"sum is {len(antinodes)}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.2f}μs")
