import time
import networkx as nx

file_path = 'input.txt'

start_time = time.perf_counter()
with open(file_path, 'r') as file:
    racetrack = []
    for line in file:
        line = line.strip()
        racetrack.append(list([char for char in line]))

start = None
end = None
empty_space = set()
for y, line in enumerate(racetrack):
    for x, char in enumerate(line):
        if char == 'S':
            start = (y,x)
            racetrack[y][x] = '.'
            char = '.'

        if char == 'E':
            end = (y,x)
            racetrack[y][x] = '.'
            char = '.'

        if char == '.':
            empty_space.add((y,x))
    #print("".join(line))

def add_dir(coord, dir):
    return (coord[0] + dir[0], coord[1] + dir[1])

all_dirs = ((0, -1), (-1, 0), (0, 1), (1, 0))
opposite_dir = {
    (0, -1): (0, 1),
    (0, 1): (0, -1),
    (-1, 0): (1, 0),
    (1, 0): (-1, 0),
}

rt = nx.Graph()
for space in empty_space:
    for facing in all_dirs:
        rt.add_node((space, facing))

for space in empty_space:
    for facing in all_dirs:
        # Transition if we don't turn
        adj = add_dir(space, facing)
        adj_char = racetrack[adj[0]][adj[1]]
        if adj_char == '.':
            rt.add_edge((space, facing), (adj, facing), weight=1)

        # Transitions to turn on the spot
        for new_facing in all_dirs:
            if new_facing == opposite_dir[facing]:
                # Never turn all the way around
                continue
            else:
                rt.add_edge((space, facing), (space, new_facing), weight=1000)

start = (start, (0,1))
ends = list([(end, dir) for dir in all_dirs])
minimum_cost = 99999999999999999
for possible_end in ends:
    try:
        cost = nx.dijkstra_path_length(rt, start, possible_end)
        if cost < minimum_cost:
            minimum_cost = cost
    except nx.exception.NetworkXNoPath:
        pass

end_time = time.perf_counter()
print(f"score is {minimum_cost}")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
