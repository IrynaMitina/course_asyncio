# tasks_on_loop.py
import asyncio
async def count_to_3(name):  # coroutine
    print(f"{name}: 1")
    await asyncio.sleep(1)  # suspend/resume
    print(f"{name}: 2")
    await asyncio.sleep(1)  # suspend/resume
    print(f"{name}: 3")


# create tasks - to schedule coroutines concurrently on event loop
async def main():
    t1 = asyncio.create_task(count_to_3("Tom"))
    t2 = asyncio.create_task(count_to_3("Jerry"))
    await t1, t2


async def main_alternative():
    await asyncio.gather(
        count_to_3("Tom"), 
        count_to_3("Jerry")
    )

# event loop runs scheduled coroutines
asyncio.run(main())
print('-----------')
asyncio.run(main_alternative())
