import time
import threading   # Used to create and manage threads

# This function will run in a separate thread
def monitor_tea_temp():
    while True:  # Infinite loop
        print("Monitoring tea temperature...")
        time.sleep(2)  # Pause execution for 2 seconds

# Create a new thread
# target → function that thread will execute
# daemon=True → thread will stop automatically when main program exits
t = threading.Thread(target=monitor_tea_temp, daemon=True)

# Start the thread
t.start()

# This line runs in the main thread
print("Main program done")


#output:
# Main program done
# Note: The monitoring thread will not keep the program alive# because it is a daemon thread. The program will exit immediately
# after printing "Main program done".