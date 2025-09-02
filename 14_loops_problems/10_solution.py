# Problem:
# Write a program to simulate a retry mechanism with exponential backoff.
# The program should:
# 1. Start with an initial wait time (e.g., 1 second).
# 2. Retry up to a maximum number of times.
# 3. After each attempt, double the wait time before the next retry.

import time

wait_time = 1
max_retries = 5
attempts = 0

while attempts < max_retries:
    print("Attempt", attempts + 1, "- wait time", wait_time, "seconds")
    time.sleep(wait_time)   # simulate waiting
    wait_time *= 2          # exponential increase
    attempts += 1
