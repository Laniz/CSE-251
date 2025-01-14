"""
Author: Brother Comeau / Brother Keers

Here is an example of using a shared queue between two threads. Note that the number of `put()`
calls must match the number of `get()` calls. If this is not the case, you will have deadlock.
"""

import threading
import queue

MAX_COUNT = 10

def read_thread(shared_q):
    for i in range(MAX_COUNT):
        # read from queue
        print(shared_q.get())

def write_thread(shared_q):
    for i in range(MAX_COUNT):
        # place value onto queue
        shared_q.put(i)

def main():
    """ Main function """

    shared_q = queue.Queue()

    write = threading.Thread(target=write_thread, args=(shared_q,))
    read = threading.Thread(target=read_thread, args=(shared_q,))

    read.start()        # doesn't matter which starts first
    write.start()

    write.join()		# Doesn't matter the order
    read.join()

if __name__ == '__main__':
    main()