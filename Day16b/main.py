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

def generate_edges(spaces):
    for space in spaces:
        for facing in all_dirs:
            for new_facing in all_dirs:
                if new_facing == opposite_dir[facing]:
                    # Never turn all the way around
                    continue

                adj = (space[0] + new_facing[0], space[1] + new_facing[1])
                adj_char = racetrack[adj[0]][adj[1]]
                if adj_char == '.':
                    if facing == new_facing:
                        yield (space, facing), (adj, facing), 1
                    else:
                        yield (space, facing), (adj, new_facing), 1001

    for facing in all_dirs:
        yield (end, facing), end, 0

rt = nx.Graph()
rt.add_weighted_edges_from(generate_edges(empty_space))
start = (start, (0,1))
costs_from_start = nx.single_source_dijkstra(rt, start, weight='weight')[0]
minimum_cost = costs_from_start[end]
costs_from_end = nx.single_source_dijkstra(rt, end, cutoff=minimum_cost, weight='weight')[0]

nodes_on_minimum_path = set()
for middle, cost_from_start in costs_from_start.items():
    try:
        cost_from_end = costs_from_end[middle]
        if cost_from_start + cost_from_end == minimum_cost:
            nodes_on_minimum_path.add(middle[0])
    except KeyError:
        pass

end_time = time.perf_counter()
print(f"score is {len(nodes_on_minimum_path)-1}") #saw {count} paths")
print(f"minimum cost is {minimum_cost}")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
