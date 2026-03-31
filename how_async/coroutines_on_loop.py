# coroutines_on_loop.py
import asyncio
async def count_to_3(name):  # coroutine
    print(f"{name}: 1")
    await asyncio.sleep(1)  # suspend/resume
    print(f"{name}: 2")
    await asyncio.sleep(1)  # suspend/resume
    print(f"{name}: 3")

async def main():
    await count_to_3("Tom")
    await count_to_3("Jerry")

asyncio.run(main())  # run event loop