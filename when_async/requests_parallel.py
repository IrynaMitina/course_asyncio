import time
import requests
import threading
URLs = ["http://google.com", "https://httpbin.org/delay/2", "https://httpbin.org/delay/1"]


def fetch(url):
    res = requests.get(url)
    if 200 != res.status_code:
        raise Exception(f"ERROR: failed to get url={url}")
    return res.text


def main():
    results = []  # can do smth with results
    threads = []
    for url in URLs:
        t = threading.Thread(target=fetch, args=(url,)) 
        threads.append(t)  
        t.start()
    for t in threads:  
        t.join()


if __name__ == '__main__':
    start_ts = time.time()
    main()
    end_ts = time.time()
    print(f"executed in {end_ts-start_ts:.2f} sec")
