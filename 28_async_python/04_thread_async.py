import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
# NOTE: spelling fix -> concurrent (not concurrrent)


def check_stock(item):
    """
    This is a normal (blocking) function.
    It simulates checking stock from a database or external service.
    """
    print(f"Checking {item} in store...")

    # This blocks the thread for 3 seconds
    # If run directly in async code, it would block the event loop
    time.sleep(3)

    return f"{item} stock: 42"


async def main():
    """
    Main async function.
    It runs a blocking function safely using a thread executor.
    """

    # Get the currently running event loop
    loop = asyncio.get_running_loop()

    # Create a ThreadPoolExecutor
    # Blocking code will run in a separate thread
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool,          # Thread pool to use
            check_stock,   # Blocking function
            "Masala chai"  # Argument passed to the function
        )

    # Print the result after the thread finishes execution
    print(result)


# Start the asyncio event loop and run main()
asyncio.run(main())


# Output:
# Checking Masala chai in store...  
# (3 second pause)
# Masala chai stock: 42
