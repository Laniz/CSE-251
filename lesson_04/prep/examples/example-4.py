"""
Author: Brother Comeau / Brother Keers

The best fix to the race condition from Example 2, is to remove the race condition. In the three
threads, they are all updating the same variable. The fix is to have each thread have it's own
variable to update. These variables will be totaled after the threads are finished.
"""

import threading, time

THREADS = 3
ITEMS = 1000000

def thread_function(data, index):
    for i in range(ITEMS):
        data[index] += 1

def main():    
    data = [0] * THREADS   # Each thread uses it's own index into the list
    start_time = time.perf_counter()

    # Create threads
    threads = [threading.Thread(target=thread_function, args=(data, index)) for index in range(THREADS)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f'All work completed: {sum(data):,} in {time.perf_counter() - start_time:.5f} seconds')

if __name__ == '__main__':
    main()