"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: <your name>

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can NOT use sleep() statements.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable from the buffer>, end=', ', flush=True)

Add any comments for me:

"""

import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2

HEAD_INDEX = BUFFER_SIZE
TAIL_INDEX = BUFFER_SIZE + 1
NEXT_VALUE = BUFFER_SIZE + 2
TOTAL_ITEMS = BUFFER_SIZE + 3
ITEMS_RECEIVED = BUFFER_SIZE + 4
WRITERS_FINISHED = BUFFER_SIZE + 5

def writer(shared_buffer, write_lock, empty_sem, full_sem):
    while True:
        empty_sem.acquire()
        
        with write_lock:
            current_value = shared_buffer[NEXT_VALUE]
            
            if current_value > shared_buffer[TOTAL_ITEMS]:
                shared_buffer[WRITERS_FINISHED] = 1
                empty_sem.release()
                break  

            write_index = shared_buffer[TAIL_INDEX]
            shared_buffer[write_index] = current_value
            shared_buffer[TAIL_INDEX] = (write_index + 1) % BUFFER_SIZE
            shared_buffer[NEXT_VALUE] = current_value + 1

        full_sem.release()

def reader(shared_buffer, read_lock, full_sem, empty_sem, items_received_lock):
    while True:
        full_sem.acquire()
        
        with items_received_lock:
            if shared_buffer[ITEMS_RECEIVED] >= shared_buffer[TOTAL_ITEMS] and shared_buffer[WRITERS_FINISHED]:
                full_sem.release()
                break  

        with read_lock:
            read_index = shared_buffer[HEAD_INDEX]
            value = shared_buffer[read_index]
            shared_buffer[HEAD_INDEX] = (read_index + 1) % BUFFER_SIZE

        empty_sem.release()

        with items_received_lock:
            shared_buffer[ITEMS_RECEIVED] += 1
            if shared_buffer[ITEMS_RECEIVED] >= shared_buffer[TOTAL_ITEMS]:
                print(value, end='', flush=True)  
              
                for _ in range(READERS):
                    full_sem.release()
                break
            
            else:
                print(value, end=', ', flush=True) 

def main():
    # total_items_to_send = 1003
    total_items_to_send = random.randint(1000, 10000)
    
    smm = SharedMemoryManager()
    smm.start()

    shared_buffer = smm.ShareableList([0] * (BUFFER_SIZE + 6))
    shared_buffer[HEAD_INDEX] = 0
    shared_buffer[TAIL_INDEX] = 0
    shared_buffer[NEXT_VALUE] = 1
    shared_buffer[TOTAL_ITEMS] = total_items_to_send
    shared_buffer[ITEMS_RECEIVED] = 0
    shared_buffer[WRITERS_FINISHED] = 0

    write_lock = mp.Lock()
    read_lock = mp.Lock()
    items_received_lock = mp.Lock()
    empty_sem = mp.Semaphore(BUFFER_SIZE)
    full_sem = mp.Semaphore(0)

    writers = [mp.Process(target=writer, args=(shared_buffer, write_lock, empty_sem, full_sem)) for _ in range(WRITERS)]
    readers = [mp.Process(target=reader, args=(shared_buffer, read_lock, full_sem, empty_sem, items_received_lock)) for _ in range(READERS)]

    for process in writers + readers:
        process.start()

    for process in writers + readers:
        process.join()

    print(f"\n{total_items_to_send} values sent")
    print(f"{shared_buffer[ITEMS_RECEIVED]} values received\n")

    smm.shutdown()

if __name__ == '__main__':
    main()