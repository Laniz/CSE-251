"""
Author: Brother Keers

This script demonstrates the concept of a lock protecting a "critical section"
of code. This is a contrived example that demonstrates what is happening on your
computer when using a lock and IS NOT how a lock should be used in your code.

- What can you infer from the output?
- Why is it important to acquire() and release() the lock as soon as possible?

INSTRUCTOR NOTE: This demo is in Lesson 1 and 2.
"""

import threading
import time


def thread_function(name, lock):
    """ Visualize what is happening when you use lock in a thread. """

    print(f'👋 I am {name}.')
    if lock.acquire(blocking=False):
        print(f'🔒 {name} has acquired the lock.')
        time.sleep(3.5)
        lock.release()
        print(f'🔓 {name} has released the lock.')
    else:
        print(f'🚫 {name} lock unavailable! Going to blocked queue.')
        while not lock.acquire(blocking=False):
            print(f'⏳ {name} still waiting for the lock.')
            time.sleep(0.9)
        print(f'🔒 {name} has acquired the lock.')
        time.sleep(1)
        lock.release()
        print(f'🔓 {name} has released the lock.')


def main():
    # Add some space in the terminal.
    print()

    # Get an instance of the thread lock.
    lock = threading.Lock()

    # Create two threads.
    t1 = threading.Thread(target=thread_function, args=("Thread-1", lock))
    t2 = threading.Thread(target=thread_function, args=("Thread-2", lock))

    # Start the threads.
    t1.start()
    t2.start()

    # Join the threads if the user choose to.
    t1.join()
    t2.join()

    # Do something else here in the main thread.
    print('✅ Demo done.\n')

if __name__ == "__main__":
    # Run the actual demo.
    main()
