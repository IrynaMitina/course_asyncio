"""
pip install psutil

# process.num_ctx_switches() - The number voluntary and involuntary context switches performed by this process (cumulative)
"""
import threading
import time
import psutil
import os

N = 500  # number of tasks

process = psutil.Process(os.getpid())
memory_initial = process.memory_info().rss


def worker():
    time.sleep(5)

threads = []
for _ in range(N):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

memory = process.memory_info().rss  # rss memory in bytes
ctx_switches = process.num_ctx_switches()  # number of context switches voluntary and involuntary , cumulative

memory_usage = (memory - memory_initial) / (1024.0 * 1024.0)
context_switches = ctx_switches.voluntary + ctx_switches.involuntary
print(f"[async] memory usage: {memory_usage:.2f} MB")
print(f"[async] context switches: {context_switches}")