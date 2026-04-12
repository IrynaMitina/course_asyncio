"""run server with: 
% uvicorn server:app --reload --host 127.0.0.1 --port 8000 --workers 1 

send requests:
% curl http://127.0.0.1:8000/cpu_best
% curl http://127.0.0.1:8000/cpu_better
% curl http://127.0.0.1:8000/cpu_bad

and check server's logs.
"""

from time import time
from concurrent.futures import ProcessPoolExecutor
import asyncio
from fastapi import FastAPI
import aiodebug.log_slow_callbacks
aiodebug.log_slow_callbacks.enable(2)


app = FastAPI()

@app.on_event("startup")
async def enable_slow_tasks_logging():
    pass
    #event_loop = asyncio.get_running_loop()
    #event_loop.set_debug(True)  # enable debug mode for event loop
    #event_loop.slow_callback_duration = 2  # in sec. - log only tasks that block event loop for more than X sec


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
    start_ts = time()
    a = fibonacci(36)
    b = fibonacci(36)
    c = fibonacci(36)
    end_ts = time()
    print(f"cpu_bad done processing in {end_ts-start_ts:.2f} sec")
    return {"message": a+b+c}


@app.get("/cpu_better")
async def cpu_better():
    print("cpu_better is invoked")
    start_ts = time()
    # allow to switch execution to another task!
    a = fibonacci(36)  # this is blocking
    await asyncio.sleep(1)  # mark place to switch
    b = fibonacci(36)
    await asyncio.sleep(1)
    c = fibonacci(36)
    end_ts = time()
    print(f"cpu_better done processing in {end_ts-start_ts:.2f} sec")
    return {"message": a+b+c}


def calc():
    a = fibonacci(36)
    b = fibonacci(36)
    c = fibonacci(36)
    return a + b + c


@app.get("/cpu_best")
async def cpu_best():
    print("cpu_best is invoked")
    start_ts = time()
    # do calculations in separate process (not thread! remember GIL !)
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, calc)
    end_ts = time()
    print(f"cpu_best done processing in {end_ts-start_ts:.2f} sec")
    return {"message": result}
