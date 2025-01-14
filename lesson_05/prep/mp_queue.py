import multiprocessing as mp 

MAX_COUNT = 10

def read_thread(shared_q):
    for i in range(MAX_COUNT):
        # read from queue
        print(f'📖 Reading: {shared_q.get()}')

def write_thread(shared_q):
    for i in range(MAX_COUNT):
        # place value onto queue
        print(f'📥 Placing: {i}')
        shared_q.put(i)

def main():
    """ Main function """

    # This queue will be shared between the processes
    shared_q = mp.Queue()

    write = mp.Process(target=write_thread, args=(shared_q,))
    read = mp.Process(target=read_thread, args=(shared_q,))

    """
    It doesn't matter which starts first, but the most efficient solution would be to start the
    writer first so the reader has something to read right away.
    """
    read.start()
    write.start()

    write.join()
    read.join()

if __name__ == '__main__':
    main()