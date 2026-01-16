import threading

chai_stock = 0  # Global variable (shared by multiple threads)

def restock():
    global chai_stock
    for _ in range(100000):
        # PROBLEM:
        # This line is NOT thread-safe.
        # Multiple threads can read, modify, and write chai_stock at the same time.
        # This causes a RACE CONDITION.
        chai_stock += 1

# Create 2 threads that run restock() simultaneously
threads = [
    threading.Thread(target=restock)
    for _ in range(2)
]

# Start both threads
for t in threads:
    t.start()

# Wait until both threads finish execution
for t in threads:
    t.join()

# EXPECTED OUTPUT:
# Chai stock: 200000
#
# ACTUAL OUTPUT (will vary each run):
# Chai stock: 132456
# Chai stock: 178923
# Chai stock: 199876
#
# Reason:
# Increment operation (+= 1) is not atomic.
# Threads overwrite each other’s updates.

print("Chai stock:", chai_stock)
