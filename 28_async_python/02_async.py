# concurrently means jab ek task wait karta hai, doosra task chal jata hai

import asyncio
import time

# This is an async function (coroutine)
async def brew(name):
    print(f"Brewing {name}...")   # Start brewing chai

    # Non-blocking delay of 3 seconds
    # During this wait, event loop can run other tasks
    await asyncio.sleep(3)

    # If we used time.sleep(3), it would block the whole program
    # time.sleep(3)

    print(f"{name} is ready...")  # Chai is ready


# Main async function
async def main():
    # asyncio.gather runs multiple async functions concurrently
    await asyncio.gather(
        brew("Masala chai"),
        brew("Green chai"),
        brew("Ginger chai"),
    )


# Starts the event loop and runs main()
asyncio.run(main())



# Output:
# Brewing Masala chai...
# Brewing Green chai...
# Brewing Ginger chai...
# (wait ~3 seconds)
# Masala chai is ready...
# Green chai is ready...
# Ginger chai is ready...
