import time

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
    return secret

score = 0
for original_secret in monkey_secrets:
    secret = original_secret
    for i in range(2000):
        secret = next_secret(secret)

    #print(f"{original_secret}: {secret}")
    score += secret

total_end_time = time.perf_counter()
print(f"score is {score}")

time_in_microseconds = (total_end_time-total_start_time) * 1000000
print(f"took {time_in_microseconds:.0f}μs")
