import asyncio
import aiohttp

# This async function fetches a single URL
async def fetch_url(session, url):
    # Send an async GET request
    async with session.get(url) as response:
        # Print URL and HTTP status code after response is received
        print(f"Fetched {url} with status {response.status}")


# Main async function
async def main():
    # Creating a list with the same URL repeated 3 times
    urls = ["https://httpbin.org/delay/2"] * 3

    # Creating a single HTTP session (best practice)
    async with aiohttp.ClientSession() as session:
        
        # Creating async tasks for each URL
        # All tasks are created immediately (not executed one by one)
        tasks = [fetch_url(session, url) for url in urls]
        
        # Run all tasks concurrently and wait for all to finish
        await asyncio.gather(*tasks)


# Start the asyncio event loop and run main()
asyncio.run(main())


Fetched https://httpbin.org/delay/2 with status 200
Fetched https://httpbin.org/delay/2 with status 200
Fetched https://httpbin.org/delay/2 with status 200
