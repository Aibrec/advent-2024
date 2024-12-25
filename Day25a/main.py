import time
import bisect

file_path = 'input.txt'

start_time = time.perf_counter()

with open(file_path, 'r') as file:
    keys = []
    locks = []

    current_type = None
    current = [-1,-1,-1,-1,-1]
    for line in file:
        line = line.strip()
        if not line:
            if current_type == 'key':
                keys.append(tuple(current))
            else:
                locks.append(tuple(current))

            current = [-1,-1,-1,-1,-1]
            current_type = None

        else:
            if current_type is None:
                if line == '.....':
                    current_type = 'key'
                else:
                    current_type = 'lock'

            for i, char in enumerate(line):
                if char == '#':
                    current[i] += 1

    if current_type:
        if current_type == 'key':
            keys.append(tuple(current))
        else:
            locks.append(tuple(current))

sorted_locks_by_tumbler = []
for tumbler in range(5):
    by_height = []
    for height in range(6):
        by_height.append(set())

    for lock in locks:
        height = lock[tumbler]
        for h in range(height, 6):
            by_height[h].add(lock)
    sorted_locks_by_tumbler.append(by_height)

score = 0
for key in keys:
    possible_lock_sets = set.intersection(*[sorted_locks_by_tumbler[tumbler][6 - key[tumbler] - 1] for tumbler in range(5)])
    score += len(possible_lock_sets)

end_time = time.perf_counter()
print(f"score {score}")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
