import time
import threading   # Used to create and manage threads

# This function will run in a separate thread
def monitor_tea_temp():
    while True:  # Infinite loop
        print("Monitoring tea temperature...")
        time.sleep(2)  # Pause execution for 2 seconds

# Create a new thread
# target → function that thread will execute
t = threading.Thread(target=monitor_tea_temp)

# Start the thread
t.start()

# This line runs in the main thread
print("Main program done")

#output:
# Monitoring tea temperature...
# Main program done
# Monitoring tea temperature...
# Monitoring tea temperature... (Infinite loop continues)
