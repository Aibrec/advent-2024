import time

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    problems = []
    for line in file:
        parts = line.split(':')
        numbers = parts[1].split()
        problems.append((int(parts[0]), tuple([int(n) for n in numbers])))

def reverse_concatenation(l, r):
    if str(l)[-1*len(str(r)):] == str(r):
        l_without_r = str(l)[:-1*len(str(r))]
        if l_without_r == '':
            return False
        return int(l_without_r)
    else:
        return False

def solve_problem_backward(target, current, numbers):
    if current == target and not numbers:
        return True

    if current < target or not numbers:
         return False

    next_number = numbers[-1]

    if current_without_next := reverse_concatenation(current, next_number):
        if result := solve_problem_backward(target, current_without_next, numbers[:-1]):
            return result

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
