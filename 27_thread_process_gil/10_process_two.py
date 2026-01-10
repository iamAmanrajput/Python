"""
Note:
Using multiprocessing allows TRUE parallelism for CPU-bound tasks.
Each process runs independently with its own Python interpreter and GIL,
so multiple CPU cores can be utilized effectively.
"""

from multiprocessing import Process
import time


def cpu_heavy():
    """
    A CPU-bound function that performs heavy computation.
    """
    print("Crunching numbers...")
    total = 0
    for i in range(10**7):  # Heavy CPU computation
        total += i
    print("Done crunching numbers.")


if __name__ == "__main__":
    # Record start time
    start = time.time()

    # Create 4 processes for the CPU-heavy task
    # Each process can run on a separate CPU core
    processes = [Process(target=cpu_heavy) for _ in range(4)]

    # Start all processes
    for p in processes:
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    # Record end time
    end = time.time()

    # Print total execution time
    print(f"Total time taken: {end - start:.2f} seconds")


# Crunching numbers...
# Crunching numbers...
# Crunching numbers...
# Crunching numbers...
# Done crunching numbers.
# Done crunching numbers.
# Done crunching numbers.
# Done crunching numbers.
# Total time taken: 1.90 seconds
