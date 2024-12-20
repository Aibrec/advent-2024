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

all_dirs = ((0, -1), (-1, 0), (0, 1), (1, 0))
def generate_edges(spaces):
    for space in spaces:
        for dir in all_dirs:
            adj = (space[0] + dir[0], space[1] + dir[1])
            adj_char = racetrack[adj[0]][adj[1]]
            if adj_char == '.':
                yield space, adj

rt = nx.Graph()
rt.add_edges_from(generate_edges(empty_space))

costs_from_start = nx.single_source_dijkstra(rt, start)[0]
target_length = (costs_from_start[end]) - 100

costs_from_end = nx.single_source_dijkstra(rt, end, cutoff=target_length)[0]

max_jump = 2

helpful_jumps = 0
for middle, cost_from_start in costs_from_start.items():
    for dy in range(-1*max_jump,max_jump+1):
        max_x = max_jump - abs(dy)
        for dx in range(-1*max_x,max_x+1):
            try:
                jump_end = (middle[0] + dy, middle[1] + dx)
                cost_to_end = costs_from_end[jump_end]
                total_cost = abs(dy)+abs(dx)+cost_from_start+cost_to_end
                if total_cost <= target_length:
                    helpful_jumps += 1
            except KeyError:
                pass

end_time = time.perf_counter()
print(f"score is {helpful_jumps}")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
