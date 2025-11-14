# Parallelism Example
#  Is code me hum 3 processes create kar rahe hain, jisme har process brew_chai() ko independently run karta hai.
#  Multiprocessing har process ko alag CPU core par chalne deta hai, isliye teeno tasks real same-time (parallel) me execute hote hain.
#  Main program join() ke through wait karta hai, aur jab teeno processes ka kaam khatam ho jata hai tab last message print hota hai.

from multiprocessing import Process
import time

# -------------------------------------------------------
# Function: Chai brewing
# This simulates a CPU/long task for multiprocessing
# -------------------------------------------------------
def brew_chai(name):
    print(f"Start of {name} chai brewing")
    time.sleep(3)
    print(f"End of {name} chai brewing")

# -------------------------------------------------------
# Main block (required for multiprocessing on Windows)
# -------------------------------------------------------
if __name__ == "__main__":
    # Creating 3 processes (3 chai makers)
    chai_makers = [
        Process(target=brew_chai, args=(f"Chai Maker #{i+1}",))
        for i in range(3)
    ]

    # Starting all processes
    for maker in chai_makers:
        maker.start()

    # Waiting for all processes to finish
    for maker in chai_makers:
        maker.join()

    print("All chai makers finished their work!")


# Start of Chai Maker #1 chai brewing
# Start of Chai Maker #2 chai brewing
# Start of Chai Maker #3 chai brewing
# End of Chai Maker #1 chai brewing
# End of Chai Maker #2 chai brewing
# End of Chai Maker #3 chai brewing
# All chai makers finished their work!