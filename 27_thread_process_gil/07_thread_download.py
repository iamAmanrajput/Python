import threading
import requests
import time


def download(url):
    # Thread yaha se start hota hai — ek URL ko download karega
    print(f"Starting download from {url}")

    # Yeh IO-bound work hai!
    # CPU yaha sirf request send karta hai,
    # uske baad CPU free ho jata hai jab tak server response nahi bhejta.
    resp = requests.get(url)

    # Jab response aa jata hai, thread wapas active hota hai
    print(f"Finished downloading from {url}, size: {len(resp.content)} bytes")


# 3 URLs jinka download parallel me karna hai
urls = [
    "https://httpbin.org/image/jpeg",
    "https://httpbin.org/image/png",
    "https://httpbin.org/image/svg",
]

start = time.time()

threads = []

for url in urls:
    # Har URL ke liye ek alag thread banta hai
    t = threading.Thread(target=download, args=(url, ))
    t.start()   # Thread start hota hi request send kar dega
    threads.append(t)

# join() ka matlab hai: "Main tab tak wait karunga jab tak sab threads khatam na ho jaye"
for t in threads:
    t.join()

end = time.time()

# Total time — noticeable point:
# Sare downloads ek-saath (parallel) ho gaye,
# isliye time kaafi kam lagta hai (IO-bound me threads shining).
print(f"All downloads done in {end - start:.2f} seconds")


# Starting download from https://httpbin.org/image/jpeg
# Starting download from https://httpbin.org/image/png
# Starting download from https://httpbin.org/image/svg
# Finished downloading from https://httpbin.org/image/svg, size: 8984 bytes
# Finished downloading from https://httpbin.org/image/png, size: 8090 bytes
# Finished downloading from https://httpbin.org/image/jpeg, size: 35588 bytes
# All downloads done in 2.14 seconds