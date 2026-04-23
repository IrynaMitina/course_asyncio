import time
import asyncio

async def non_blocking_count(name):
    print(f"{name} 1")
    await asyncio.sleep(2)  # suspend/resume
    print(f"{name} 2")
    await asyncio.sleep(2)  # suspend/resume
    print(f"{name} 3")


async def blocking_count(name):
    print(f"{name} 1")
    time.sleep(2)  # sync code - blocks event loop for 2 sec
    print(f"{name} 2")
    time.sleep(2)  # sync code - blocks event loop for 2 sec
    print(f"{name} 3")


# create tasks - to schedule coroutines concurrently on event loop
async def blocking_main():
    await asyncio.gather(
        blocking_count("Tom"), 
        blocking_count("Jerry")
    )

async def non_blocking_main():
    await asyncio.gather(
        non_blocking_count("Tom"), 
        non_blocking_count("Jerry")
    )


# event loop runs scheduled coroutines
print("********************************** non blocking coro")
asyncio.run(non_blocking_main())

print("********************************** blocking coro")
asyncio.run(blocking_main())
