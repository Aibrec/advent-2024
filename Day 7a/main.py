import time

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    problems = []
    for line in file:
        parts = line.split(':')
        numbers = parts[1].split()
        problems.append((int(parts[0]), tuple([int(n) for n in numbers])))

def solve_problem_backward(target, current, numbers):
    if current == target and not numbers:
        return True

    if current < target or not numbers:
         return False

    next_number = numbers[-1]

    if current % next_number == 0:
        if result := solve_problem_backward(target, current//next_number, numbers[:-1]):
            return result

    if result := solve_problem_backward(target, current-next_number, numbers[:-1]):
        return result

    return False

sum = 0
for problem in problems:
    if solve_problem_backward(problem[1][0], problem[0], problem[1][1:]):
        sum += problem[0]

end = time.perf_counter()
print(f"sum is {sum}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.2f}μs")
