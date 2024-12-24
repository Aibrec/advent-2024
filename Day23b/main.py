import time
import networkx as nx
import itertools

file_path = 'input.txt'

start_time = time.perf_counter()
with open(file_path, 'r') as file:
    edges = []
    nodes_starting_t = set()
    for line in file:
        left,right = line.strip().split('-')
        edges.append((left,right))

        if left.startswith('t'):
            nodes_starting_t.add(left)

        if right.startswith('t'):
            nodes_starting_t.add(right)

party = nx.Graph()
party.add_edges_from(edges)

max_cliques = list(nx.find_cliques(party))
largest_clique = max(max_cliques, key=len)
sorted_nodes = sorted(largest_clique)

end_time = time.perf_counter()
print(f"Largest clique: {",".join(sorted_nodes)}")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
