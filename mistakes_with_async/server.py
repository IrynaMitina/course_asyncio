"""run server with: 
uvicorn server:app --reload --host 127.0.0.1 --port 8000 --workers 1 
"""

import time
from concurrent.futures import ProcessPoolExecutor
import asyncio
from fastapi import FastAPI

app = FastAPI()


################################################ CPU-heavy endpoints
def fibonacci(n: int) -> int:
    """ calculate n-th fibonacci number
    >>> fibonacci(36)
    14930352
    >>> timeit.timeit(lambda: fibonacci(36), number=1)
    1.2742970839972259  # seconds!
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@app.get("/cpu_bad")
async def cpu_bad():
    # only blocking CPU-heavy code
    print("cpu_bad is invoked")
    a = fibonacci(36)
    b = fibonacci(36)
    c = fibonacci(36)
    print("cpu_bad done processing")
    return {"message": a+b+c}


@app.get("/cpu_better")
async def cpu_better():
    print("cpu_better is invoked")
    # allow to switch execution to another task!
    a = fibonacci(36)  # this is blocking
    await asyncio.sleep(1)  # mark place to switch
    b = fibonacci(36)
    await asyncio.sleep(1)
    c = fibonacci(36)
    print("cpu_better done processing")
    return {"message": a+b+c}


def calc():
    a = fibonacci(36)
    b = fibonacci(36)
    c = fibonacci(36)
    return a + b + c


@app.get("/cpu_best")
async def cpu_best():
    print("cpu_best is invoked")
    # do calculations in separate process (not thread! remember GIL !)
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, calc)
    print("cpu_best done processing")
    return {"message": result}


################################################ I/O-heavy endpoints
@app.get("/io_bad")
async def io_bad():
    print("io_bad is invoked")
    time.sleep(3) # simulate sync call to database 
    print("io_bad done processing")
    return {"status": "io ok"}


@app.get("/io_better")
async def io_better():
    print("io_better is invoked")
    def processing():
        time.sleep(3) # simulate sync call to database 

    result = await asyncio.to_thread(processing)
    print("io_better done processing")
    return {"status": "io ok"}


@app.get("/io_best")
async def io_best():
    print("io_best is invoked")
    await asyncio.sleep(3)  # simulate async call to database
    print("io_best done processing")
    return {"status": "io ok"}
