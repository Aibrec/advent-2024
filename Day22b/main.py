import time
import functools
from collections import defaultdict
import numpy as np

file_path = 'input.txt'

total_start_time = time.perf_counter()
with open(file_path, 'r') as file:
    monkey_secrets = []
    for line in file:
        line = line.strip()
        monkey_secrets.append(int(line))

def score_table_for_secret(secret):
    last_digits = np.zeros(2001, dtype=np.int8)
    last_digits[0] = secret % 10
    for i in range(1, 2001):
        secret = (secret ^ (secret * 64)) % 16777216
        secret = (secret ^ (secret // 32)) % 16777216
        secret = (secret ^ (secret * 2048)) % 16777216
        last_digits[i] = secret % 10

    differences = np.ediff1d(last_digits)
    scores = {}
    for i in range(len(differences)-4):
        combination = tuple(differences[i:i+4])
        last_digit_after_combination = last_digits[i+4]
        if combination not in scores:
            scores[combination] = int(last_digit_after_combination)

    return scores

score = defaultdict(int)
for original_secret in monkey_secrets:
    secret_scores = score_table_for_secret(original_secret)
    for combination, value in secret_scores.items():
        score[combination] += value

most_bananas = max(score.values())

total_end_time = time.perf_counter()
print(f"most bananas is {most_bananas}")

time_in_microseconds = (total_end_time-total_start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
