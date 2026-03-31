import asyncio
import psutil
import os

N = 500  # number of tasks

process = psutil.Process(os.getpid())

async def worker():
    await asyncio.sleep(5)

async def main():
    print(f"[asyncio] before: {process.memory_info().rss / 1024 / 1024:.2f} MB")

    tasks = [asyncio.create_task(worker()) for _ in range(N)]

    await asyncio.sleep(1)  # let all tasks start
    print(f"[asyncio] during: {process.memory_info().rss / 1024 / 1024:.2f} MB")

    await asyncio.gather(*tasks)

asyncio.run(main())
