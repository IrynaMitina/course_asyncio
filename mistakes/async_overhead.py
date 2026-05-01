"""Demo async overhead related to tasks scheduling done by event loop

When there are a lot of small tasks - and time to 'await' is tiny =>
synchronous code will be faster, then async;
Since async scheduling overhead become predominant; 
Consider for example reading a lot of local files asynchronously. 
No network latency (files are local => nothing to wait.

% python read_files.py
340000 symbols
async executed in 0.29 sec
340000 symbols
sync executed in 0.02 sec
"""
import asyncio
import aiofiles
from time import time

FILES = ["a.txt", "b.txt", "c.txt"]*1000

async def read_file_async(path):
    async with aiofiles.open(path, "r") as f:
        return await f.read()


def read_file_sync(path):
    with open(path, "r") as f:
        return f.read()
    

async def main_async():
    results = await asyncio.gather(
        *(read_file_async(f) for f in FILES)
    )
    count_symbols = 0
    for r in results:
        count_symbols += len(r)
    print(f"{count_symbols} symbols")


def main_sync():
    results = [read_file_sync(f) for f in FILES]
    count_symbols = 0
    for r in results:
        count_symbols += len(r)
    print(f"{count_symbols} symbols")


start_ts = time()
asyncio.run(main_async())
print(f"async: reading files executed in {time() - start_ts:.2f} sec")


start_ts = time()
main_sync()
print(f"sync: reading files executed in {time() - start_ts:.2f} sec")
