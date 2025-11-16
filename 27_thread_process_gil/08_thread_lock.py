import threading

# Shared global variable (iske upar sab threads write karne wale hain)
counter = 0

# Lock banaya — ye ensure karega ki ek time me sirf ek thread counter change kare
lock = threading.Lock()

def increament():
    global counter
    # Har thread 1,00,000 baar counter increment karega
    for _ in range(100000):
        # 'with lock' ka matlab hai: 
        # ye block ek time me sirf ek hi thread run karega
        with lock:
            counter += 1   # critical section (shared memory update)


# 10 threads banaye jo same function increament() ko chalayenge
threads = [threading.Thread(target=increament) for _ in range(10)]

# Saare threads ko start kiya (parallel chalna shuru)
[t.start() for t in threads]

# Saare threads ke khatam hone ka wait kar rahe (main thread yaha rukta hai)
[t.join() for t in threads]

# Final counter print (should be 1,000,000)
print(f"Final counter: {counter}")


# NOTE:
# 1. Agar lock NAHI use karte to:
#    - Multiple threads ek hi time par same shared memory
#      (counter variable) ko modify karte.
#    - counter += 1 atomic operation nahi hai (read + add + write).
#    - Isliye values overwrite hoti hain -> Race Condition.
#    - Final counter hamesha WRONG aata (kabhi 10 lakh nahi aata).

# 2. Jab lock USE karte hain:
#    - Ek time me sirf ek thread hi counter ko update kar sakta hai.
#    - Dusra thread tab tak wait karta hai jab tak lock free na ho.
#    - Isse koi overwrite nahi hoti.
#    - Race Condition solve ho jati hai.
#    - Final counter ALWAYS correct hota hai (10 threads * 100000 = 1000000).
# ---------------------------------------------------------