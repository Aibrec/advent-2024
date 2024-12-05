import time
from functools import cmp_to_key

file_path = 'input.txt'

start = time.time_ns()
with open(file_path, 'r') as file:
    orderings = {}
    reached_end_of_orderings = False
    pages_to_print = []
    for line in file:
        line = line.strip()
        if not reached_end_of_orderings:
            if not line:
                reached_end_of_orderings = True
                continue
            smaller,larger = line.split('|')
            smaller = int(smaller)
            larger = int(larger)

            orderings[tuple(sorted([larger, smaller]))] = (smaller, larger)
        else:
            pages_to_print.append(list([int(i) for i in line.split(',')]))

def compare(l,r):
    if l == r:
        return 0

    sorted_numbers = tuple(sorted([l, r]))
    if sorted_numbers not in orderings:
        raise Exception('Missing ordering')

    ordering = orderings[sorted_numbers]
    if l == ordering[0]:
        return -1
    elif l == ordering[1]:
        return 1

sum = 0
for pages in pages_to_print:
    ordered_pages = sorted(pages, key=cmp_to_key(compare))
    if ordered_pages != pages:
        middle_index = int((len(ordered_pages) - 1)/2)
        middle_value = ordered_pages[middle_index]
        sum += middle_value

end = time.time_ns()
print(f"sum is {sum}")

time_in_microseconds = (end-start) / 1000
print(f"took {time_in_microseconds}μs")
