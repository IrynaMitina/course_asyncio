"""use 'async for' to iterate over asynchronous generator or iterator."""
import asyncio
import random


# custom async generator
async def async_generator(n):
    for _ in range(n):
        yield random.randint(0, 100)
        await asyncio.sleep(0.5)  # simulate waiting for next value to arrive


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
        await asyncio.sleep(0.5)  # simulate waiting for next value to arrive
        return random.randint(0, 100)


async def main():
    print("using async generator:")
    async for x in async_generator(5):
        print(x)
    print("using async iterator:")    
    async for x in AsyncIterator(5):
        print(x)


asyncio.run(main())