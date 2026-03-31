import threading
import time
import psutil
import os

N = 500  # number of tasks

process = psutil.Process(os.getpid())

def worker():
    time.sleep(5)

threads = []

print(f"[threading] before: {process.memory_info().rss / 1024 / 1024:.2f} MB")

for _ in range(N):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

time.sleep(1)
print(f"[threading] during: {process.memory_info().rss / 1024 / 1024:.2f} MB")

for t in threads:
    t.join()
