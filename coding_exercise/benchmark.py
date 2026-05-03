"""benchmark to compare performance of server endpoints."""
import random
import requests
import threading
from time import time

def fetch(url):
    res = requests.get(url)
    if 200 != res.status_code:
        raise Exception(f"ERROR: failed to get url={url}")
    return res.text

def fetch_in_parallel(urls):
    # fetch all urls in parallel using threads
    threads = []
    for url in urls:
        t = threading.Thread(target=fetch, args=(url,)) 
        threads.append(t)  
        t.start()
    for t in threads:  
        t.join()

def benchmark(urls):
    # fetch all urls in parallel using threads - measure execution time
    start_ts = time()
    fetch_in_parallel(urls)
    return time() - start_ts


def checks():
    # case#2: sync
    start_ts = time()
    took_time_1 = benchmark(
        ["http://127.0.0.1:8000/count_pairs_sync/?name1=Daniel&name2=Emma&name3=Alex&name4=Ivan",
         "http://127.0.0.1:8000/count_pairs_sync/?name1=Maxim&name2=Anna&name3=Sofia&name4=Lucas",
         "http://127.0.0.1:8000/count_pairs_sync/?name1=Olivia&name2=Maria&name3=Maxim&name4=Daniel"]
    )
    #t = threading.Thread(target=fetch, args=("http://127.0.0.1:8000/count_pairs_sync/?name1=Daniel&name2=Emma&name3=Alex&name4=Ivan",))  
    #t.start()
    #t.join()
    # took_time = benchmark([f"http://127.0.0.1:8000/user_sync/{i}" for i in ids_2])
    took_time = benchmark(
        #["http://127.0.0.1:8000/count_pairs_sync/?name1=Daniel&name2=Emma&name3=Alex&name4=Ivan"]
        #+
        [f"http://127.0.0.1:8000/ping" for i in range(100)])
    print(f"case sync: {time() - start_ts:.2f} sec total, {took_time_1:.2f} sec for count_pairs, {took_time:.2f} sec for pings")

    # case#1: async
    start_ts = time()
    took_time_1 = benchmark(
        ["http://127.0.0.1:8000/count_pairs/?name1=Daniel&name2=Emma&name3=Alex&name4=Ivan",
         "http://127.0.0.1:8000/count_pairs/?name1=Maxim&name2=Anna&name3=Sofia&name4=Lucas",
         "http://127.0.0.1:8000/count_pairs/?name1=Olivia&name2=Maria&name3=Maxim&name4=Daniel"]
    )
    #t = threading.Thread(target=fetch, args=("http://127.0.0.1:8000/count_pairs/?name1=Daniel&name2=Emma&name3=Alex&name4=Ivan",))  
    #t.start()
    #t.join()
    #took_time = benchmark([f"http://127.0.0.1:8000/user/{i}" for i in ids_1])
    took_time = benchmark(
        #["http://127.0.0.1:8000/count_pairs/?name1=Daniel&name2=Emma&name3=Alex&name4=Ivan"]
        #+
        [f"http://127.0.0.1:8000/ping" for i in range(100)])
    print(f"case async: {time() - start_ts:.2f} sec total, {took_time_1:.2f} sec for count_pairs, {took_time:.2f} sec for pings")
 

if __name__=='__main__':
    checks()
