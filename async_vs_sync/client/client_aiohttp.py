"""Client to fetch 3 URLs concurrently using aiohttp."""
import aiohttp
import asyncio
import time
URLs = ["http://google.com", "https://httpbin.org/delay/2", "https://httpbin.org/delay/1"]

async def fetch(url):
    async with aiohttp.request('GET', url) as response:
        if 200 != response.status:
            response.raise_for_status()
        return await response.text()

async def main():    
    # create tasks on event loop - to execute fetches concurrently
    tasks = []
    for url in URLs:
        task = asyncio.create_task(fetch(url))
        tasks.append(task)
    # wait for all fetches to be finished
    results = await asyncio.gather(*tasks) 
    # can do smth with results    

if __name__ == '__main__':
    start_ts = time.time()
    asyncio.run(main())  # run event loop
    end_ts = time.time()
    print(f"executed in {end_ts-start_ts:.2f} sec")
