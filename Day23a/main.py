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

three_cliques = set()
for node in nodes_starting_t:
    cliques = list(nx.find_cliques(party, nodes=[node]))
    for clique in cliques:
        if len(clique) == 3:
            three_cliques.add(frozenset(clique))
        elif len(clique) > 3:
            clique_without_node = list([n for n in clique if n != node])
            for two_clique in itertools.combinations(clique_without_node, 2):
                three_cliques.add(frozenset([node, two_clique[0], two_clique[1]]))

end_time = time.perf_counter()
print(f"3-cliques with a t-node: {len(three_cliques)}")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
