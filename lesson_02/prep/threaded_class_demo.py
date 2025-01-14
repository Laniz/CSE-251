"""
Author: Brother Keers

This script demonstrates the basics of threading with classes in python. You
should compare this example to the thread demo from the previous lessons prep
material. You should think about the following questions and discuss them with
your team:

- Why do we have to call super() here?
- What is different about the lock here compared to the previous demo?

Note that this example is meant to show you how this is done -- what the code
would look like -- and is not a great implementation of threading.
"""

import threading

class CounterThread(threading.Thread):
    """
    A simple class that extends threading.Thread and counts from 0 to 100000
    using threading.
    """
    
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.lock = threading.Lock()

    """
    NOTE: This acts as the `target` for your thread. When you use a threaded class
    calling start() on the thread will automatically call run(). Any `args` you
    need should have been taken care of in the constructor.
    """
    def run(self):
        for _ in range(100000):
            with self.lock:
                self.counter += 1

def main():
    # Create two instances of the CounterThread class
    thread1 = CounterThread()
    thread2 = CounterThread()

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for the threads to finish
    thread1.join()
    thread2.join()

    # Print the final value of the counter for each thread
    print("Thread 1 counter:", thread1.counter)
    print("Thread 2 counter:", thread2.counter)

# Protect the call to main
if __name__ == '__main__':
    main()
