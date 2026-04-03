"""script illustrating unsafe work with shared resource (global variable)."""
import asyncio

counter = 0  # shared resource - global variable

async def increment():
    global counter
    tmp = counter          # read
    await asyncio.sleep(0) # switching execution to another task happens here
    counter = tmp + 1      # write

async def main():
    tasks = [asyncio.create_task(increment()) for _ in range(1000)]
    await asyncio.gather(*tasks)
    print(counter)

asyncio.run(main()) 
