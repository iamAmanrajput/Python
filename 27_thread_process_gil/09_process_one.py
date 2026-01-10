# Note: Due to Python's Global Interpreter Lock (GIL),
# the threads will not run in true parallel for CPU-bound tasks.
# This example demonstrates that threading may not improve performance
# for CPU-bound operations in Python.

import threading
import time 

def cpu_heavy():
    print("Crunching numbers...")
    total = 0
    for i in range(10**7):  # Heavy CPU computation
        total += i
    print("Done crunching numbers.")

start = time.time()

# Creating 4 threads for a CPU-bound task
threads = [threading.Thread(target=cpu_heavy) for _ in range(4)]

# Start all threads
for t in threads:
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

end = time.time()

print(f"Total time taken: {end - start:.2f} seconds")

# Crunching numbers...
# Crunching numbers...
# Crunching numbers...
# Crunching numbers...
# Done crunching numbers.
# Done crunching numbers.
# Done crunching numbers.
# Done crunching numbers.
# Total time taken: 6.40 seconds

