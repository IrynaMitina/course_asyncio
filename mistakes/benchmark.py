"""benchmark to compare performance of server endpoints."""
import sys
import requests
import threading
from time import time

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


def compare_io_heavy_endpoints():
    # to compare performance of io-heavy endpoints:
    # we send 5 parallel requests to same io-heavy endpoint under interest
    # and measure time it takes for the server to process all 5 requests and return responses

    # which io_ is really better on server?
    # case 'io_bad' 
    # 5 parallel clients send io_bad requests
    took_time = benchmark(["http://127.0.0.1:8000/io_bad"]*5)
    print(f"case 'io_bad' - {took_time:.2f} sec")

    # case 'io_better' 
    # 5 parallel clients send io_better requests
    took_time = benchmark(["http://127.0.0.1:8000/io_better"]*5)
    print(f"case 'io_better' - {took_time:.2f} sec")

    # case 'io_best'
    # 5 parallel clients send io_best requests
    took_time = benchmark(["http://127.0.0.1:8000/io_best"]*5)
    print(f"case 'io_best' - {took_time:.2f} sec")


def compare_cpu_heavy_endpoints():
    # to compare performance of cpu-heavy endpoints:
    # we send first request to cpu-heavy endpoint that we want to estimate
    # after that we send 5 parallel requests to io_best endpoint
    # and measure time it takes for the server to return responses to all 5 requests
    
    # case 'cpu_bad first':
    # first client sends cpu_bad request, 
    # after that 5 parallel clients send io_best requests
    t = threading.Thread(target=fetch, args=("http://127.0.0.1:8000/cpu_bad",))
    t.start()
    took_time = benchmark(["http://127.0.0.1:8000/io_best"]*5)
    print(f"case 'cpu_bad first' - {took_time:.2f} sec")
    t.join()
 
    # case 'cpu_better first':
    # first client send cpu_better request, 
    # after that 5 parallel clients send io_best requests
    t = threading.Thread(target=fetch, args=("http://127.0.0.1:8000/cpu_better",))
    t.start()
    took_time = benchmark(["http://127.0.0.1:8000/io_best"]*5)
    print(f"case 'cpu_better first' - {took_time:.2f} sec")
    t.join()
    
    # case 'cpu_best first'
    # first client send cpu_best request, 
    # after that 5 parallel clients send io_best requests
    t = threading.Thread(target=fetch, args=("http://127.0.0.1:8000/cpu_best",))
    t.start()
    took_time = benchmark(["http://127.0.0.1:8000/io_best"]*5)
    print(f"case 'cpu_best first' - {took_time:.2f} sec")
    t.join()



if __name__=='__main__':
    op = sys.argv[1]
    if 'io' == op:
        compare_io_heavy_endpoints()
    elif 'cpu' == op:  # 'cpu' 
        compare_cpu_heavy_endpoints()
    else: # both
        compare_io_heavy_endpoints()
        compare_cpu_heavy_endpoints()

