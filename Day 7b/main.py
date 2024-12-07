import time

file_path = 'input.txt'

start = time.time_ns()
with open(file_path, 'r') as file:
    problems = []
    for line in file:
        parts = line.split(':')
        numbers = parts[1].split()
        problems.append((int(parts[0]), tuple([int(n) for n in numbers])))

def concatenation(l, r):
    return int(str(l) + str(r))

def solve_problem(target, current, numbers):
    if target == current and not numbers:
        return current

    if target < current or not numbers:
        return 0

    next_number = numbers[0]
    if result := solve_problem(target, next_number+current, numbers[1:]):
        return result
    elif result := solve_problem(target, next_number*current, numbers[1:]):
        return result
    else:
        return solve_problem(target, concatenation(current, next_number), numbers[1:])

sum = 0
for problem in problems:
    sum += solve_problem(problem[0], problem[1][0], problem[1][1:])

end = time.time_ns()
print(f"sum is {sum}")

time_in_microseconds = (end-start) / 1000
print(f"took {time_in_microseconds}μs")
