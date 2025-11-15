from multiprocessing import Process
import time

def crunch_number():
    print("Started the count process...")
    count = 0
    for _ in range(100_000_000):
        count += 1
    print("Ended the count process...")


if __name__ == "__main__":
    start = time.time()

    p1 = Process(target=crunch_number)
    p2 = Process(target=crunch_number)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    end = time.time()

    print(f"Total time with multi-processing is {end - start:.2f} seconds")


# output
# Started the count process...
# Ended the count process...
# Ended the count process...
# Total time with multi-processing is 2.78 seconds



# ===========================================================
#                     GIL NOTES (IMPORTANT)
# ===========================================================
#
# In this code, GIL has NO role.
# Multiprocessing completely bypasses the GIL.
#
# WHY? (Simple Version)
# ---------------------
# Each process has its own Python interpreter and its own GIL.
#
# Threading:
#     1 process  +  1 GIL  + many threads
#
# Multiprocessing:
#     N processes  +  N GILs (each process has its own)
#
# Har process apni independent memory
# aur apna independent interpreter use karta hai.
#
# Therefore:
#     👉 Dono processes TRUE PARALLEL chal sakte hain
#     👉 GIL ek process ko block nahi karta
#     👉 CPU-bound work fastest hota hai
#     👉 Total time almost half ho jata hai (example: 2.78 sec)
#
# ===========================================================
