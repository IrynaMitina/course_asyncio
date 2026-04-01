"""benchmark to compare performance: fastapi (async) vs. flask (sync) servers.

It runs 10 parallel clients that send requests to fastapi server.
Prints how much time it took for all clients to get responses.
Then it does the same for flask server.
Before running benchmark - start both servers.
"""
# benchmarking_fastapi.py
import requests
import threading
from time import time

N = 10


def fetch(url):
    res = requests.get(url)
    if 200 != res.status_code:
        raise Exception(f"ERROR: failed to get url={url}")
    return res.text


def benchmark(urls):
    # fetch all urls in parallel using threads - measure execution time
    start_ts = time()
    threads = []
    for url in urls:
        t = threading.Thread(target=fetch, args=(url,)) 
        threads.append(t)  
        t.start()
    for t in threads:  
        t.join()
    return time() - start_ts
    

if __name__=='__main__':
    took_time = benchmark(["http://127.0.0.1:8000/"]*N)
    print(f"fastapi server: took {took_time:.2f} sec (to process {N} parallel clients)")

    took_time = benchmark(["http://127.0.0.1:8001/"]*N)
    print(f"flask server: took {took_time:.2f} sec (to process {N} parallel clients)")