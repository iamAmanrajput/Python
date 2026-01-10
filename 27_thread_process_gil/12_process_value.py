# The program creates a shared counter using Value
# Four processes run at the same time
# Each process increases the counter 100,000 times
# A lock is used so that processes do not update the counter together
# This avoids wrong values (race condition)
# At the end, the counter correctly shows 400,000

from multiprocessing import Process, Value

def increment(counter):
    """
    This function increases the shared counter value.
    Each process runs this function and increments
    the counter 100,000 times.
    """
    for _ in range(100000):
        # Lock ensures that only one process
        # updates the counter at a time
        with counter.get_lock():
            counter.value += 1


if __name__ == "__main__":
    # Create a shared integer variable with initial value 0
    # This value can be accessed and modified by all processes
    counter = Value('i', 0)

    # Create multiple processes that run the same function
    p1 = Process(target=increment, args=(counter,))
    p2 = Process(target=increment, args=(counter,))
    p3 = Process(target=increment, args=(counter,))
    p4 = Process(target=increment, args=(counter,))

    # Start all processes
    p1.start()
    p2.start()
    p3.start()
    p4.start()

    # Wait for all processes to finish execution
    p1.join()
    p2.join()
    p3.join()
    p4.join()

    # Print the final value of the counter
    # Expected value: 4 processes × 100000 = 400000
    print("Final Counter Value:", counter.value)



# Final Counter Value: 400000
