"""script illustrating safe work with shared resource (global variable)."""
import asyncio

counter = 0  # shared resource - global variable
lock = asyncio.Lock()

async def increment():
    # asquired lock should be released before it could be asquired again!
    global counter
    async with lock:  # asquire lock
        tmp = counter
        await asyncio.sleep(0)  # switching execution to another task happens here
        counter = tmp + 1

async def main():
    tasks = [asyncio.create_task(increment()) for _ in range(1000)]
    await asyncio.gather(*tasks)
    print(counter)

asyncio.run(main())
