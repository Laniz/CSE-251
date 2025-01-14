"""
Author: Brother Comeau / Brother Keers

Same program as Example 1 but looping 1,000,000 times. The results should be 3,000,000, but it isn't.
In fact, each time the the program is run, different results are displayed. This is caused by a race
condition for the first element in the list.
"""

import threading, time

THREADS = 3
ITEMS = 1000000

def thread_function(data):
    for i in range(ITEMS):
        data[0] += 1

def main():    
    data = [0]
    start_time = time.perf_counter()

    # Create threads
    threads = [threading.Thread(target=thread_function, args=(data, )) for _ in range(THREADS)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f'All work completed: {data[0]:,} in {time.perf_counter() - start_time:.5f} seconds')

if __name__ == '__main__':
    main()