""" benchmark for using green threads (async) in case of high concurrency.

measures memory footprint, and number of context switching during OS threads management.
"""
import asyncio
import psutil
import os

N = 500  # number of tasks

process = psutil.Process(os.getpid())
memory_initial = process.memory_info().rss


async def worker():
    await asyncio.sleep(5)

async def main():
    tasks = [asyncio.create_task(worker()) for _ in range(N)]
    await asyncio.gather(*tasks)

asyncio.run(main())

memory = process.memory_info().rss  # rss memory in bytes
ctx_switches = process.num_ctx_switches()  # number of context switches voluntary and involuntary , cumulative

memory_usage = (memory - memory_initial) / (1024.0 * 1024.0)
context_switches = ctx_switches.voluntary + ctx_switches.involuntary
print(f"[async] memory usage: {memory_usage:.2f} MB")
print(f"[async] context switches: {context_switches}")
