# Deadlock Example in Python
import threading
import time

# Two locks (shared resources)
lock_a = threading.Lock()
lock_b = threading.Lock()

def task1():
    # Task 1 acquires lock_a first
    with lock_a:
        print("Task 1 acquired lock A")
        time.sleep(1)  # Delay to increase chances of deadlock

        # Task 1 now tries to acquire lock_b
        with lock_b:
            print("Task 1 acquired lock B")

def task2():
    # Task 2 acquires lock_b first
    with lock_b:
        print("Task 2 acquired lock B")
        time.sleep(1)  # Delay to increase chances of deadlock

        # Task 2 now tries to acquire lock_a
        with lock_a:
            print("Task 2 acquired lock A")

# Create threads
t1 = threading.Thread(target=task1)
t2 = threading.Thread(target=task2)

# Start threads
t1.start()
t2.start()

# Wait for threads to complete
t1.join()
t2.join()

print("Main program finished")

# EXPECTED OUTPUT:
# Task 1 acquired lock A
# Task 2 acquired lock B
# (Program hangs here due to deadlock)