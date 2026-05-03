"""Script illustrating safe & unsafe work with shared resource (global variable)."""
import asyncio

counter = 0  # shared resource - global variable
lock = asyncio.Lock()

async def safe_increment():
    # get exclusive lock to work with shared resource alone!
    # no other task can get/asquire the lock until it will be released
    global counter
    async with lock:  # asquire lock
        tmp = counter
        # unsafe (with 'await') critical section - execution can switch here to another task
        await asyncio.sleep(0)
        counter = tmp + 1


async def unsafe_increment():
    # not using sync primitives to provide safe work with shared resource
    global counter
    tmp = counter          # read
    # unsafe (with 'await') critical section - execution can switch here to another task
    await asyncio.sleep(0)
    counter = tmp + 1      # write


async def safe_main():
    tasks = [asyncio.create_task(safe_increment()) for _ in range(1000)]
    await asyncio.gather(*tasks)
    print(f"safe increment: counter={counter}")


async def unsafe_main():
    tasks = [asyncio.create_task(unsafe_increment()) for _ in range(1000)]
    await asyncio.gather(*tasks)
    print(f"unsafe increment: counter={counter}")


counter = 0  # reset counter
asyncio.run(safe_main())

counter = 0  # reset counter
asyncio.run(unsafe_main())