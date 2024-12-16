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

rt = nx.DiGraph()
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

rt.add_node(end)
for facing in all_dirs:
    rt.add_edge((end, facing), end, weight=0)

start = (start, (0,1))
minimum_cost = nx.dijkstra_path_length(rt, start, end)

costs_from_start = nx.single_source_dijkstra(rt, start, cutoff=minimum_cost, weight='weight')[0]

reverse_rt = nx.reverse(rt)
costs_from_end = nx.single_source_dijkstra(reverse_rt, end, cutoff=minimum_cost, weight='weight')[0]
nodes_on_minimum_path = set()
for middle, cost_from_start in costs_from_start.items():
    if middle[0] not in nodes_on_minimum_path:
        if middle in costs_from_end:
            cost_from_end = costs_from_end[middle]
            if cost_from_start + cost_from_end == minimum_cost:
                nodes_on_minimum_path.add(middle[0])

end_time = time.perf_counter()
print(f"score is {len(nodes_on_minimum_path)-1}") #saw {count} paths")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
