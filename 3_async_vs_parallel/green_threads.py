"""
2 tasks: "Tom counts to 3" and "Jerry counts to 3" - run concurrently on event loop.
"""
import asyncio
async def count_to_3(name):  # coroutine
    print(f"{name}: 1")
    await asyncio.sleep(4)  # suspend/resume
    print(f"{name}: 2")
    await asyncio.sleep(4)  # suspend/resume
    print(f"{name}: 3")


# create tasks - to schedule coroutines concurrently on event loop
async def main():
    await asyncio.gather(
        count_to_3("Tom"), 
        count_to_3("Jerry")
    )

# event loop runs scheduled coroutines
asyncio.run(main())