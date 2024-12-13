import time
from collections import defaultdict

file_path = 'input.txt'

start = time.perf_counter()
with open(file_path, 'r') as file:
    machines = []
    current_machine = []
    for line in file:
        if len(current_machine) < 2:
            parts = line.strip().split()
            x = int((parts[2].split('+'))[1][:-1])
            y = int((parts[3].split('+'))[1])
            current_machine.append((y,x))
        elif len(current_machine) == 2:
            parts = line.strip().split()
            x = int((parts[1].split('='))[1][:-1])
            y = int((parts[2].split('='))[1])
            current_machine.append((y, x))
        else:
            machines.append(current_machine)
            current_machine = []

# Index 0 is A, index 1 is B, index 2 is the prize location
cost = (3, 1)

def solve_machine(a, b, prize):
    # From linear algebra
    clicks_A = (prize[1]*b[0] - prize[0]*b[1]) // (a[1]*b[0] - b[1]*a[0])
    clicks_B = (prize[0] - (clicks_A*a[0])) // b[0]

    # Check answer as fractions aren't usable
    check_answer = (a[0]*clicks_A + b[0]*clicks_B, a[1]*clicks_A + b[1]*clicks_B)
    if check_answer != prize:
        return 0

    return 3*clicks_A + 1*clicks_B

total = 0
for machine in machines:
    total += solve_machine(machine[0], machine[1], machine[2])

end = time.perf_counter()
print(f"sum is {total}")

time_in_microseconds = (end-start) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
