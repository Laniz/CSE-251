"""
Author: Brother Keers

In this example an unbounded Queue is being created and then used by an equal
amount of threads. 5 items are added to the Queue and then 5 threads are spun up
to each process 1 item from the queue. Since there is an equal pairing of queue
items to threads we don't need to lock anything or add a flag indicating the
queue has reached the end. There really is no need for a queue in this example.

You should think about the following questions and discuss them with your team:

- Why is this an impractical example? *hint* It is!
- What happens at the hardware level if you change ITEM_COUNT to a big number?
"""

import queue
import threading

ITEM_COUNT = 5

def thread_function(q):
    size = q.qsize()
    item = q.get()
    print(f'Thread: {item:<5} Current Queue Size: {size}')


def main():
    q = queue.Queue()

    # Put some items in the queue.
    for i in range(1, ITEM_COUNT + 1):
        q.put(i)

    # Create a thread for every item in the queue.
    threads = []
    for _ in range(ITEM_COUNT):
        threads.append(threading.Thread(target=thread_function, args=(q, )))

    # Start all threads.
    for i in range(ITEM_COUNT):
        threads[i].start()

    # Wait for them to finish.
    for i in range(ITEM_COUNT):
        threads[i].join()

    # Show that we have successfully processed the queue.
    print(f'All work completed. Queue size is now: {q.qsize()}')


if __name__ == '__main__':
    main()