import time
import functools

file_path = 'input.txt'

start_time = time.perf_counter()
with open(file_path, 'r') as file:
    available_towels = None
    for line in file:
        line = line.strip()
        if not line:
            break

        available_towels = list(line.split(', '))
        available_towels.sort(key=len)
        available_towels = tuple(available_towels)

    combinations = []
    for line in file:
        combinations.append(line.strip())

@functools.cache
def find_matching_towels_from_start(available_towels, combination):
    if not combination:
        return 1

    num_valid = 0
    for towel in available_towels:
        if combination.startswith(towel):
            num_valid += find_matching_towels_from_end(available_towels, combination[len(towel):])
    return num_valid

@functools.cache
def find_matching_towels_from_end(available_towels, combination):
    if not combination:
        return 1

    num_valid = 0
    for towel in available_towels:
        if combination.endswith(towel):
            num_valid += find_matching_towels_from_start(available_towels, combination[:-1*len(towel)])
    return num_valid

def solve(available_towels, combinations):
    possible_combos = 0
    for i, combination in enumerate(combinations):
        num_valid = find_matching_towels_from_start(available_towels, combination)
        possible_combos += num_valid
        # if i % 10 == 0:
        #     print(f'Done {i}/{len(combinations)}')
    return possible_combos

result = solve(available_towels, combinations)
end_time = time.perf_counter()
print(f"score {result}")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
