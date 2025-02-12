"""
Course: CSE 251 
Lesson: L05 Prove
File:   prove.py
Author: Shepherd Ncube

Purpose: Assignment 05 - Factories and Dealers

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You MUST use a barrier!
- Do not use try...except statements.
- You are not allowed to use the normal Python Queue object. You must use Queue251.
- The shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE.
"""

from datetime import datetime, timedelta
import time
import threading
import random

from cse251 import *

MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

class Car():
    # Class attributes for makes, models, and years.
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep',
                 'Subaru', 'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan',
                 'Toyota', 'Lexus', 'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')
    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat',
                  'Middle', 'Round', 'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand',
                  'Viper', 'F150', 'Town', 'Ranger', 'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')
    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)
        # Sleep a bit to simulate work
        time.sleep(random.random() / SLEEP_REDUCE_FACTOR)
        print(f'Created: {self.info()}')
           
    def info(self):
        return f'{self.make} {self.model}, {self.year}'

class Queue251():
    def __init__(self):
        self.__items = []
        self.__max_size = 0

    def get_max_size(self):
        return self.__max_size

    def put(self, item):
        self.__items.append(item)
        if len(self.__items) > self.__max_size:
            self.__max_size = len(self.__items)

    def get(self):
        return self.__items.pop(0)

class Factory(threading.Thread):
    def __init__(self, queue, semaphore1, semaphore2, barrier, factory_id, factory_count, dealer_count):
        super().__init__()
        self.queue = queue
        self.banana1 = semaphore1
        self.banana2 = semaphore2
        self.barrier = barrier
        self.factory_id = factory_id      
        self.factory_count = factory_count
        self.dealer_count = dealer_count
        self.cars_to_produce = random.randint(200, 300)  # DO NOT change

    def run(self):
        # Produce the cars.
        for _ in range(self.cars_to_produce):
            self.banana1.acquire()
            car = Car()
            self.queue.put(car)
            self.banana2.release()

        # Compute how many termination signals (-1) to produce.
        # This ensures that in total exactly one -1 is enqueued for each dealer.
        sentinels = self.dealer_count // self.factory_count
        if self.factory_id < (self.dealer_count % self.factory_count):
            sentinels += 1

        for _ in range(sentinels):
            self.banana1.acquire()
            self.queue.put(-1)  
            self.banana2.release()

        # Use the barrier to signal that this factory is done.
        self.barrier.wait()

class Dealer(threading.Thread):
    def __init__(self, queue, semaphore1, semaphore2, dealer_stats, index, barrier):
        super().__init__()
        self.queue = queue
        self.banana1 = semaphore1
        self.banana2 = semaphore2
        self.dealer_stats = dealer_stats
        self.index = index
        self.barrier = barrier

    def run(self):
        while True:
            self.banana2.acquire()
            item = self.queue.get()
            
            if item == -1:
                break

            print(f'Sold: {item.info()}')
            self.dealer_stats[self.index] += 1
            self.banana1.release()
            time.sleep(random.random() / SLEEP_REDUCE_FACTOR)

        # Use the barrier to signal that this dealer is done.
        self.barrier.wait()

def run_production(factory_count, dealer_count):
    # Create the semaphores used to control access to the queue.
    banana1 = threading.Semaphore(MAX_QUEUE_SIZE)
    banana2 = threading.Semaphore(0)
    car_queue = Queue251()
    dealer_stats = [0] * dealer_count

    # Create a barrier that waits for all factories and dealers.
    barrier = threading.Barrier(factory_count + dealer_count)

    # Create factory and dealer threads, passing in the barrier and counts.
    factories = [Factory(car_queue, banana1, banana2, barrier, i, factory_count, dealer_count)
                 for i in range(factory_count)]
    dealers = [Dealer(car_queue, banana1, banana2, dealer_stats, i, barrier)
               for i in range(dealer_count)]

    log.start_timer()

    # Start all dealer threads.
    for dealer in dealers:
        dealer.start()
    # Start all factory threads.
    for factory in factories:
        factory.start()

    # Wait for all factories and dealers to finish.
    for factory in factories:
        factory.join()
    for dealer in dealers:
        dealer.join()

    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created.')
    factory_stats = [factory.cars_to_produce for factory in factories]

    return (run_time, car_queue.get_max_size(), dealer_stats, factory_stats)

def main(log):
    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)
        # print(' ')
        # print(f'Factories      : {factories}')
        # print(f'Dealerships    : {dealerships}')
        # print(f'Run Time       : {run_time:.4f}')
        # print(f'Max queue size : {max_queue_size}')
        # print(' ')

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factory Stats  : Made = {sum(factory_stats)} @ {factory_stats}')
        log.write(f'Dealer Stats   : Sold = {sum(dealer_stats)} @ {dealer_stats}')
        log.write('')


if __name__ == '__main__':
    log = Log(show_terminal=True)
    main(log)
