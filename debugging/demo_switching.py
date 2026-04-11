"""This is to demo visually how execution flow switches between 2 coroutines on the event loop.

Set breakpoints in both coroutines after 'await' line 
(place where execution resumes).
Run debugging, press step over each time execution stops.
"""
import asyncio

async def calc_a():
    a = 0
    await asyncio.sleep(1)  # suspend/resume
    a += 1
    await asyncio.sleep(1)  # suspend/resume
    a += 3
    await asyncio.sleep(1)  # suspend/resume
    a = a + 5
    return a


async def calc_b():
    b = 0
    await asyncio.sleep(1)  # suspend/resume
    b += 2
    await asyncio.sleep(1)  # suspend/resume
    b += 4
    await asyncio.sleep(1)  # suspend/resume
    b = b + 6
    return b


# create tasks - to schedule coroutines concurrently on event loop
async def main():
    t1 = asyncio.create_task(calc_a())
    t2 = asyncio.create_task(calc_b())
    await t1, t2


# event loop runs scheduled coroutines
asyncio.run(main())