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
        return True

    start_towels = match_against_trie(combination)
    for towel in start_towels:
        if find_matching_towels_from_start(combination[len(towel):]):
            return True

    return False

valid_combos = 0
for i, combination in enumerate(combinations):
    matching_towels = find_matching_towels_from_start(combination)
    if matching_towels:
        #print(f"matched {combination}")
        valid_combos += 1

end_time = time.perf_counter()
print(f"score {valid_combos}")

time_in_microseconds = (end_time-start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
