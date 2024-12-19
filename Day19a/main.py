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

        available_towels = tuple(line.split(', '))

    combinations = []
    for line in file:
        combinations.append(line.strip())

@functools.cache
def find_matching_towels(available_towels, combination):
    for start_towel in available_towels:
        if combination.startswith(start_towel):
            remaining_combination = combination[len(start_towel):]
            if not remaining_combination:
                return [start_towel]

            for end_towel in available_towels:
                if combination.endswith(end_towel):
                    remaining_combination = remaining_combination[:-1*len(end_towel)]

                    if not remaining_combination:
                        return [start_towel, end_towel]
                    elif matching := find_matching_towels(available_towels, remaining_combination):
                        matching.extend([start_towel, end_towel])
                        return matching
    return None

@functools.cache
def find_matching_towels_from_start(available_towels, combination):
    if not combination:
        return True

    for towel in available_towels:
        if combination.startswith(towel):
            if find_matching_towels_from_end(available_towels, combination[len(towel):]):
                return True

    return False

@functools.cache
def find_matching_towels_from_end(available_towels, combination):
    if not combination:
        return True

    for towel in available_towels:
        if combination.endswith(towel):
            if find_matching_towels_from_start(available_towels, combination[:-1*len(towel)]):
                return True

    return False

valid_combos = 0
for i, combination in enumerate(combinations):
    matching_towels = find_matching_towels(available_towels, combination)
    if matching_towels:
        valid_combos += 1

end_time = time.perf_counter()
print(f"score {valid_combos}")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
