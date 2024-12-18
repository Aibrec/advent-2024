import time
import networkx as nx

file_path = 'input.txt'

start_time = time.perf_counter()
with open(file_path, 'r') as file:
    blocked_spots = set()
    counter = 0
    for line in file:
        x,y = line.strip().split(',')
        blocked_spots.add((int(y), int(x)))
        counter += 1
        if counter == 1024:
            break

all_dirs = ((0, -1), (-1, 0), (0, 1), (1, 0))
def generate_edges(max_y, max_x, blocked_spots):
    for y in range(max_y+1):
        for x in range(max_x+1):
            space = (y,x)
            if space not in blocked_spots:
                for dir in all_dirs:
                    adj = (space[0] + dir[0], space[1] + dir[1])
                    if adj not in blocked_spots:
                        yield space, adj

max_x = 70
max_y = 70

memory = nx.Graph()
memory.add_edges_from(generate_edges(max_y, max_x, blocked_spots))

start = (0,0)
end = (max_y, max_x)

costs_from_start = nx.shortest_path(memory, start, end)

end_time = time.perf_counter()
print(f"score is {len(costs_from_start)-1}")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
