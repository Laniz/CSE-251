import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting(id):
    print(f'Cleaner: {id} waiting...')
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner: {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting(id):
    print(f'Guest: {id} waiting...')
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count}')
    time.sleep(random.uniform(0, 1))

def cleaner(id, room_lock, clean_count, stop_time):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    while time.time() < stop_time:
        cleaner_waiting(id)
        with room_lock:
            print(STARTING_CLEANING_MESSAGE)
            cleaner_cleaning(id)
            print(STOPPING_CLEANING_MESSAGE)
            clean_count.value += 1

def guest(id, room_lock, guest_count, party_count, stop_time):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (call guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    while time.time() < stop_time:
        guest_waiting(id)
        with room_lock:
            if guest_count.value == 0:
                print(STARTING_PARTY_MESSAGE)
                party_count.value += 1
            guest_count.value += 1
        
        guest_partying(id, guest_count.value)
        
        with room_lock:
            guest_count.value -= 1
            if guest_count.value == 0:
                print(STOPPING_PARTY_MESSAGE)

def main():
    # Start time of the running of the program. 
    start_time = time.time()
    stop_time = start_time + TIME

    # Shared variables
    room_lock = mp.Lock()
    guest_count = mp.Value('i', 0)
    clean_count = mp.Value('i', 0)
    party_count = mp.Value('i', 0)

    # Create cleaner and guest processes
    processes = []
    for i in range(CLEANING_STAFF):
        p = mp.Process(target=cleaner, args=(i, room_lock, clean_count, stop_time))
        processes.append(p)
        p.start()

    for i in range(HOTEL_GUESTS):
        p = mp.Process(target=guest, args=(i, room_lock, guest_count, party_count, stop_time))
        processes.append(p)
        p.start()
    
    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Results
    print(f'Room was cleaned {clean_count.value} times, there were {party_count.value} parties')

if __name__ == '__main__':
    main()