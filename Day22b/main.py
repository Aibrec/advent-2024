import time
from collections import defaultdict

file_path = 'input.txt'

total_start_time = time.perf_counter()
with open(file_path, 'r') as file:
    monkey_secrets = []
    for line in file:
        line = line.strip()
        monkey_secrets.append(int(line))

def next_secret(secret):
    secret = (secret ^ (secret * 64)) % 16777216
    secret = (secret ^ (secret // 32)) % 16777216
    secret = (secret ^ (secret * 2048)) % 16777216
    last_digit = secret % 10
    return secret, last_digit

def score_table_for_secret(secret):
    last_four_differences = [None, None, None, None]
    scores = {}
    previous_last_digit = secret % 10

    for i in range(3):
        secret, last_digit = next_secret(secret)
        last_four_differences[i] = last_digit - previous_last_digit
        previous_last_digit = last_digit

    for i in range(4, 2001):
        secret, last_digit = next_secret(secret)
        last_four_differences[3] = last_digit - previous_last_digit
        if (combination := tuple(last_four_differences)) not in scores:
            scores[combination] = last_digit

        previous_last_digit = last_digit
        last_four_differences[0] = last_four_differences[1]
        last_four_differences[1] = last_four_differences[2]
        last_four_differences[2] = last_four_differences[3]

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
