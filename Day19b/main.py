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

    combinations = []
    for line in file:
        combinations.append(line.strip())

trie_of_available_towels = {
    'string': '',
    'next': {}
}

def add_towel(towel):
    level = trie_of_available_towels
    for i, char in enumerate(towel):
        if char not in level['next']:
            level['next'][char] = {}
            level['next'][char]['next'] = {}
            level['next'][char]['string'] = level['string'] + char
            level['next'][char]['length'] = len(level['next'][char]['string'])
            level['next'][char]['is_a_towel'] = False
        level = level['next'][char]
    level['is_a_towel'] = True

for towel in available_towels:
    add_towel(towel)

def match_against_trie(combination):
    node = trie_of_available_towels
    valid_towels = []
    for char in combination:
        if char not in node['next']:
            break

        node = node['next'][char]
        if node['is_a_towel']:
            valid_towels.append(node['string'])
    return valid_towels

@functools.cache
def find_matching_towels_from_start(combination):
    if not combination:
        return 1

    num_valid = 0
    start_towels = match_against_trie(combination)
    for towel in start_towels:
        num_valid += find_matching_towels_from_start(combination[len(towel):])
    return num_valid

def solve(available_towels, combinations):
    possible_combos = 0
    for i, combination in enumerate(combinations):
        num_valid = find_matching_towels_from_start(combination)
        possible_combos += num_valid
    return possible_combos

result = solve(available_towels, combinations)
end_time = time.perf_counter()
print(f"score {result}")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
