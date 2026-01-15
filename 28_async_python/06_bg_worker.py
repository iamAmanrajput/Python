import asyncio
import threading
import time


def background_worker():
    """
    This function runs in a separate background thread.
    It continuously logs system health every 1 second.
    """
    while True:
        time.sleep(1)  # Pause for 1 second (blocking sleep)
        print("Logging the system health 🕰️")


async def fetch_orders():
    """
    Async function that simulates fetching orders.
    It does NOT block the main thread.
    """
    await asyncio.sleep(3)  # Non-blocking sleep
    print("🎁 order fetched")


# Start a background thread for system monitoring
# daemon=True means this thread will stop when the main program exits
threading.Thread(
    target=background_worker,
    daemon=True
).start()


# Run the asyncio event loop to execute the async task
asyncio.run(fetch_orders())

# Output:
# Logging the system health 🕰️ 
# Logging the system health 🕰️
# Logging the system health 🕰️
# 🎁 order fetched