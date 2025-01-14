"""
Author: Brother Keers

In this example an unbounded Queue is being created and then used by a 2 threads.
The 2 threads will process the items as fast as possible and then automatically
quit when they reach a flag indicating there are no more items in the queue to
process. Note that we add 2 additional items (q.put(None) x 2) to the queue
because we used 2 threads.

You should think about the following questions and discuss them with your team:

- Would it be possible to bound the queue in this example?
- What happens at the hardware level if you change ITEM_COUNT to a big number?
- What if we used 3 threads? What would we need to change?
- Remove the 2 `q.put(None)` lines of code and run again. Why did it deadlock?
"""

import queue
import threading

ITEM_COUNT = 25

def thread_function(q, thread_number):
    """ Pretend to do some work with an item from the queue. """
    while True:
        size = q.qsize()
        item = q.get()
        if item == None:
            return
        print(f'Thread: {thread_number:<5} Current Queue Size: {size}')


def main():
    q = queue.Queue()

    # Put some items in the queue.
    for i in range(1, ITEM_COUNT + 1):
        q.put(i)

    # We must add a "flag" of some kind to indicate to our threads the queue is empty.
    q.put(None)
    q.put(None)

    # Create 2 threads that will process (work through) the queue.
    t1 = threading.Thread(target=thread_function, args=(q, 1))
    t2 = threading.Thread(target=thread_function, args=(q, 2))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Show that we have successfully processed the queue.
    print(f'All work completed. Queue size is now: {q.qsize()}')


if __name__ == '__main__':
    main()