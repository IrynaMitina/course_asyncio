from time import sleep
import threading 
workers = 2
 
def count_to_3(name):
    print(f"{name}: 1")
    sleep(4)
    print(f"{name}: 2")
    sleep(4)
    print(f"{name}: 3")


def main():
    threads = []
    for name in ("Tom", "Jerry"):
        t = threading.Thread(target=count_to_3, args=(name,)) 
        threads.append(t)  
        t.start()
    for t in threads:  
        t.join()


main()