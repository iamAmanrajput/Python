import threading
import time


def brew_chai():
    # NOTE: Ye line thread ka name print karegi.
    print(f"{threading.current_thread().name} started brewing...")

    # NOTE: Yeh ek heavy CPU-bound loop hai. 
    # Is loop ke har iteration me Python bytecode execute hota hai,
    # aur Python bytecode run karne ke liye GIL (mutex) chahiye hota hai.
    count = 0
    for _ in range(200_000_000):
        count += 1

    # NOTE: Yeh tab print hoga jab thread apna poora loop complete kar lega.
    print(f"{threading.current_thread().name} finished brewing...")


# --------------------------
# Main thread
# --------------------------

# 1) Do threads create ho rahe hain.
# NOTE: Thread banate hi ye RUN nahi honge, ye bas "ready" state me hote hain.
thread1 = threading.Thread(target=brew_chai, name="Barista-1")
thread2 = threading.Thread(target=brew_chai, name="Barista-2")

start = time.time()

# 2) Dono threads start ho rahe hain.
# NOTE: Start hote hi dono threads GIL lene ki koshish karenge.
#       Lekin GIL ek mutex hai → ek time par sirf ek thread ko CPU deta hai.
thread1.start()
thread2.start()

# 3) join() means main thread wait karega jab tak ye threads khatam nahi ho jate.
thread1.join()
thread2.join()

end = time.time()

print(f"Total time taken: {end - start:.2f} seconds")


# Barista-1 started brewing...
# Barista-2 started brewing...
# Barista-1 finished brewing...
# Barista-2 finished brewing...
# Total time taken: 11.95 seconds


"""
==========================
   GIL (Mutex) Notes
==========================

- Python me ek global mutex hota hai jise GIL (Global Interpreter Lock) kehte hain.
- GIL ensure karta hai ki ek time par SIRF 1 thread Python bytecode execute kare.

Aage code me kya ho raha hai:

1) Barista-1 start hota hai
   → GIL acquire karta hai
   → Apne loop ke kuch milliseconds tak iterations run karta hai.

2) Python forcefully GIL chhod deta hai
   → Ye isliye hota hai taaki fairness maintain rahe,
     aur doosra thread bhi run ho sake.

3) Ab Barista-2 GIL acquire karta hai
   → Barista-2 apne loop ke kuch iterations run karta hai.

4) Fir GIL release hota hai
   → Barista-1 wapas GIL lekar apna loop continue karta hai.

5) Ye switching bahut fast hoti hai:
      Barista-1 → GIL → run
      Barista-1 → release
      Barista-2 → GIL → run
      Barista-2 → release
      (repeat...)

NOTE:
- Baar-baar switching se "concurrency" milti hai but "parallelism" nahi.
- CPU-bound code hamesha slow hoga multi-threading me, kyunki 
  GIL ek time par ek hi thread ko loop execute karne deta hai.

Total time ≠ half
Total time ≈ 2x single-thread time
"""

