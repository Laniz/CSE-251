"""
Author: Brother Keers

This script demonstrates the basics of threading in python. You should think
about the following questions and discuss them with your team:

- What can you infer from the output?
- Why do the results differ with or without thread.join()?
"""

import sys
import threading
import time

def thread_function(name):
    print(f'Thread {name} is running')
    time.sleep(2)
    print(f'Thread {name} is finished')


def main(join_threads):
    # Notify the user of what demo is about to run.
    if join_threads:
        print(f'\n{"-" * 18}')
        print('DEMO: Join threads')
        print('-' * 18)
    else:
        print(f'\n{"-" * 25}')
        print('DEMO: DO NOT join threads')
        print('-' * 25)

    # Create two threads.
    t1 = threading.Thread(target=thread_function, args=("Thread-1",))
    t2 = threading.Thread(target=thread_function, args=("Thread-2",))

    # Start the threads.
    t1.start()
    t2.start()

    # Join the threads if the user choose to.
    if join_threads:
        t1.join()
        t2.join()

    # Do something else here in the main thread.
    print('Doing something else in the main thread')


if __name__ == "__main__":
    # Check the command line arguments for the join flag.
    join_threads = False
    if 'join' in sys.argv:
        join_threads = True

    # Run the actual demo.
    main(join_threads)
