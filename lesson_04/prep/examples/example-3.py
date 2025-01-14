"""
Author: Brother Comeau / Brother Keers

We can fix the race condition in Example 2 by adding a lock around `data[0] += 1`. We got the right
answer with adding a lock, but the execution time of the program is now 5 seconds.
"""

import threading, time

THREADS = 3
ITEMS = 1000000

def thread_function(lock, data):
    for i in range(ITEMS):
        with lock:
            data[0] += 1

def main():    
    lock = threading.Lock()
    data = [0]
    start_time = time.perf_counter()

    # Create threads
    threads = [threading.Thread(target=thread_function, args=(lock, data)) for _ in range(THREADS)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f'All work completed: {data[0]:,} in {time.perf_counter() - start_time:.5f} seconds')

if __name__ == '__main__':
    main()