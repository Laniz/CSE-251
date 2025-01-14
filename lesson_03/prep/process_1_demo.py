"""
Author: Brother Keers

This script demonstrates the concept of using multithread processes to do
something. In this demo we attempt to update a global variable inside the
processes. Notice how you can use processes in a similar fashion to threads.

- Why did the global counter not update? *hint* Read the prep material!
- If the processes run in parallel why does the output print in the same order
  we started the processes in? In other words, why does 1 print before 2?
"""

import multiprocessing as mp

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

    # Both workers are finished show the ending counter.
    print('🏁 All workers finished.')
    print(f'🔢 Global counter is at: {counter}\n')
