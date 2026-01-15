import asyncio
from concurrent.futures import ProcessPoolExecutor


def encrypt(data):
    """
    This is a CPU-bound synchronous function.
    It simulates encryption by reversing the string.
    """
    # Reverse the string using slicing
    return f"🔒 {data[::-1]}"


async def main():
    """
    Main async function.
    It runs a CPU-bound task in a separate process
    using ProcessPoolExecutor.
    """

    # Get the currently running asyncio event loop
    loop = asyncio.get_running_loop()

    # Create a ProcessPoolExecutor
    # CPU-heavy work will run in a separate process
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool,          # Process pool to use
            encrypt,       # CPU-bound function
            "credit_card_1234"  # Argument passed to the function
        )

    # Print the result returned from the process
    print(result)


if __name__ == "__main__":
    # Start the asyncio event loop and run main()
    asyncio.run(main())


# ---------------- OUTPUT ----------------
# 🔒 4321_drac_tiderc
#
# Explanation of output:
# Original string  : credit_card_1234
# Reversed string  : 4321_drac_tiderc
# Lock emoji (🔒)  : Just to represent "encrypted" data
# ---------------------------------------
