import time
from numbers import Number

file_path = 'input.txt'

start = time.time_ns()
with open(file_path, 'r') as file:
    problems = []
    for line in file:
        parts = line.split(':')
        numbers = parts[1].split()
        problems.append((int(parts[0]), tuple([int(n) for n in numbers])))

def solve_problem_backward(current, numbers):
    if current == 0 and not numbers:
        return True

    if current < 0 or not numbers:
         return False

    next_number = numbers[-1]
    if result := solve_problem_backward(current-next_number, numbers[:-1]):
        return result

    if current % next_number == 0:
        if result := solve_problem_backward(current//next_number, numbers[:-1]):
            return result

    return False

sum = 0
for problem in problems:
    if solve_problem_backward(problem[0], problem[1]):
        sum += problem[0]

end = time.time_ns()
print(f"sum is {sum}")

time_in_microseconds = (end-start) / 1000
print(f"took {time_in_microseconds}μs")
