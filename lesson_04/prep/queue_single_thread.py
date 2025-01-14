"""
Author: Brother Keers

In this example an unbounded Queue is being created and then used by a single
thread. This is a bad example because it allows us to cheat and call `queue.get()`
without any ramifications, plus we can rely on `queue.qsize()` which is not
thread safe normally! We also don't need to lock anything or add a flag indicating
the queue has reached the end. There really is no need for a a queue in this example.

You should think about the following questions and discuss them with your team:

- Would it be possible to bound the queue in this example?
- What happens at the hardware level if you change ITEM_COUNT to a big number?
"""

import queue
import threading

ITEM_COUNT = 10

def thread_function(q):
    """ Pretend to do some work with an item from the queue. """
    size = q.qsize()
    while size > 0:
        item = q.get()
        print(f'Thread: {"1":<5} Current Queue Size: {size}')
        size -= 1


def main():
    q = queue.Queue()

    # Put some items in the queue.
    for i in range(1, ITEM_COUNT + 1):
        q.put(i)

    # Create a thread for every item in the queue.
    thread = threading.Thread(target=thread_function, args=(q, ))
    thread.start()
    thread.join()

    # Show that we have successfully processed the queue.
    print(f'All work completed. Queue size is now: {q.qsize()}')


if __name__ == '__main__':
    main()