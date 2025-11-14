# concurrecy example
# Python me concurrency ka matlab hai ek hi CPU core multiple threads ko fast switching ke through chalata hai — jab ek thread wait (sleep) karta hai, CPU turant dusre thread ko run karta hai.

import threading
import time

# -------------------------------------------------------
# Function 1: Taking orders
# This simulates an I/O-bound task (wait + print)
# -------------------------------------------------------
def take_orders():
    for i in range(1, 4):
        print(f"Taking order for #{i}")
        time.sleep(1)  # simulating wait time (I/O wait)

# -------------------------------------------------------
# Function 2: Brewing chai
# Another I/O-bound task (wait + print)
# -------------------------------------------------------
def brew_chai():
    for i in range(1, 4):
        print(f"Brewing chai for #{i}")
        time.sleep(2)  # simulating a longer wait time

# -------------------------------------------------------
# Creating threads
# Each thread will run one function independently
# -------------------------------------------------------
order_thread = threading.Thread(target=take_orders)
brew_thread = threading.Thread(target=brew_chai)

# -------------------------------------------------------
# Starting both threads
# This allows take_orders() and brew_chai() to run concurrently
# -------------------------------------------------------
order_thread.start()
brew_thread.start()

# -------------------------------------------------------
# join() waits until each thread finishes
# This ensures the main program doesn’t exit early
# -------------------------------------------------------
order_thread.join()
brew_thread.join()

print("All tasks completed!")


# Taking order for #1
# Brewing chai for #1
# Taking order for #2
# Brewing chai for #2
# Taking order for #3
# Brewing chai for #3
# All tasks completed!
