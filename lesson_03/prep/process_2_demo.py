"""
Author: Brother Keers

This is the same demo as `process_1_demo.py` but we added a thread that calls
the process() function as well.

- Why did the global counter change this time? *hint* Read the prep material!
"""

import multiprocessing as mp
import threading

counter = 0

def process(name):
    """ worker function that normally would do something. """
    global counter
    print(f'🟢 {name} started.')
    print(f'📦 {name} updating global counter.')
    counter += 1
    print(f'🔴 {name} finished.')


if __name__ == '__main__':
    # Print the initial counter.
    print(f'\n🔢 Global counter is at: {counter}')

    # Create two worker processes
    p1 = mp.Process(target=process, args=('Process 1',))
    p2 = mp.Process(target=process, args=('Process 2',))

    # Start the worker processes
    p1.start()
    p2.start()

    # Join the worker processes
    p1.join()
    p2.join()

    # Now do the same thing but with a thread instead.
    t1 = threading.Thread(target=process, args=('Thread 1',))
    t1.start()
    t1.join()

    # All workers are finished show the ending counter.
    print('🏁 All workers finished.')
    print(f'🔢 Global counter is at: {counter}\n')
