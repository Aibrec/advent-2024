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
for i in range(5):
    sorted_locks = sorted(locks, key=lambda lock: lock[i])
    sorted_locks_by_tumbler.append(sorted_locks)

score = 0
for key in keys:
    possible_locks = None
    for tumbler in range(5):
        overlap_on_tumbler = 6 - key[tumbler]
        too_high_index = bisect.bisect_left(sorted_locks_by_tumbler[tumbler], overlap_on_tumbler, key=lambda lock: lock[tumbler])
        sublist_of_valid_locks = sorted_locks_by_tumbler[tumbler][:too_high_index]
        if possible_locks is None:
            possible_locks = set(sublist_of_valid_locks)
        else:
            possible_locks = possible_locks.intersection(sublist_of_valid_locks)
            if len(possible_locks) == 0:
                break
    score += len(possible_locks)

# This was half as fast but so much simpler
# score = 0
# for l, lock in enumerate(locks):
#     for k, key in enumerate(keys):
#         for i in range(5):
#             if (lock[i] + key[i]) >= 6:
#                 break
#         else:
#             score += 1

end_time = time.perf_counter()
print(f"score {score}")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
