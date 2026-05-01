"""This is to demo execution flow during async iteration.

Prints were added to highlight execution flow.
Run script with `python async_for.py` and analyze the output.
Notice how during iteration in 'async for' loop - execution switches from 
generator to iterator (and back), and to other coroutines."""
import asyncio
import random


# custom async generator
async def async_generator(n):
    for _ in range(n):
        print("gen: suspending")
        await asyncio.sleep(0.5)  # simulate waiting for next value to arrive
        print("gen: resuming")
        yield random.randint(0, 100)


# custom async iterator
class AsyncIterator:
    def __init__(self, n):
        self.i = n

    def __aiter__(self):  # returns an asynchronous iterator object
        return self
    
    async def __anext__(self):  # coroutine that returns the next value or raises StopAsyncIteration when done
        if self.i <= 0:
            raise StopAsyncIteration
        self.i -= 1
        print("iter: suspending")
        await asyncio.sleep(0.5)  # simulate waiting for next value to arrive
        print("iter: resuming")
        return random.randint(0, 100)


async def coro_iterate_generator():
    async for x in async_generator(3):
        print(f"gen {x}")


async def coro_iterate_iterator():
    async for x in AsyncIterator(3):
        print(f"iter {x}")


async def main():
    await asyncio.gather(
        coro_iterate_generator(),
        coro_iterate_iterator()
    )

asyncio.run(main())