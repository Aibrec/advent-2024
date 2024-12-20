import time
import array

file_path = 'input.txt'

total_start_time = time.perf_counter()
y_len = 0
x_len = None
start = None
end = None
with (open(file_path, 'r') as file):
    racetrack = array.array('l')
    for line in file:
        line = line.strip()
        if (s_loc := line.find('S')) != -1:
            start = (y_len, s_loc)

        if (s_loc := line.find('E')) != -1:
            end = (y_len, s_loc)

        x_len = len(line)
        y_len += 1
        racetrack.fromlist(list([-1 if char=='#' else 1 for char in line]))

all_dirs = ((0, -1), (-1, 0), (0, 1), (1, 0))
no_180_dirs = {
    (0, -1): ((0, -1), (1, 0), (-1, 0)),
    (0, 1): ((0, 1), (1, 0), (-1, 0)),
    (-1, 0): ((-1, 0), (0, 1), (0, -1)),
    (1, 0): ((1, 0), (0, 1), (0, -1)),
}

def find_starting_dir(start):
    for dir in all_dirs:
        adj = (start[0] + dir[0], start[1] + dir[1])
        adj_char = racetrack[adj[0]*x_len + adj[1]]
        if adj_char == 1:
            return dir

def find_line(start, end):
    line = [start]
    next = start
    current_dir = find_starting_dir(start)
    while next != end:
        for next_dir in no_180_dirs[current_dir]:
            adj = (next[0] + next_dir[0], next[1] + next_dir[1])
            adj_char = racetrack[adj[0]*x_len + adj[1]]
            if adj_char == 1:
                next = adj
                current_dir = next_dir
                line.append(next)
                break
        else:
            raise Exception('Line broken')
    line.append(end)
    return line

line = find_line(start, end)
for i, node in enumerate(line):
    racetrack[node[0] * x_len + node[1]] = len(line) - i

max_jump = 20
helpful_jumps = 0
for i, node in enumerate(line):
    nodes_remaining_cost_to_end = len(line) - i
    for dy in range(-1*min(max_jump, node[0]), min(max_jump+1, y_len-node[0])):
        max_x_jump = max_jump - abs(dy)
        for dx in range(-1*min(max_x_jump, node[1]), min(max_x_jump+1, x_len-node[1])):
            end_of_jump_cost = racetrack[(node[0] + dy)*x_len + node[1] + dx]
            if end_of_jump_cost == -1:
                continue

            saved_cost = nodes_remaining_cost_to_end - (abs(dy)+abs(dx)+end_of_jump_cost)
            if saved_cost >= 100:
                helpful_jumps += 1


total_end_time = time.perf_counter()
print(f"score is {helpful_jumps}")

time_in_microseconds = (total_end_time-total_start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
