"""Client to fetch 3 URLs sequentially using requests."""
import time
import requests
URLs = ["http://google.com", "https://httpbin.org/delay/2", "https://httpbin.org/delay/1"]

def fetch(url):
    res = requests.get(url)
    if 200 != res.status_code:
        raise Exception(f"ERROR: failed to get url={url}")
    return res.text

def main():
    results = []
    for url in URLs:
        results.append(fetch(url))
    # can do smth with results
        
if __name__ == '__main__':
    start_ts = time.time()
    main()
    end_ts = time.time()
    print(f"executed in {end_ts-start_ts:.2f} sec")
