import time
import threading
import random
from datetime import datetime

# Include cse 251 common Python files
from cse251 import *

# Global Constants - DO NOT CHANGE
cars_to_be_made = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        print(f'Created: {self.info()}')
           
    def info(self):
        """ Helper function to quickly get the car information. """
        return f'{self.make} {self.model}, {self.year}'


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.__items = []

    def size(self):
        return len(self.__items)

    def put(self, item):
        assert len(self.__items) <= 10
        self.__items.append(item)

    def get(self):
        return self.__items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, queue, banana1, sem_full):
        threading.Thread.__init__(self)
        self.queue = queue
        self.banana1 = banana1
        # banana1 is a semaphore it counts the number of available slots in the queue
        self.sem_full = sem_full

    def run(self):
        for _ in range(cars_to_be_made):
            self.banana1.acquire()  
            car = Car()
            self.queue.put(car)
            self.sem_full.release()  
        

class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, queue, banana1, sem_full, queue_stats):
        threading.Thread.__init__(self)
        self.queue = queue
        self.banana1 = banana1
        self.sem_full = sem_full
        self.queue_stats = queue_stats

    def run(self):
        for _ in range(cars_to_be_made):
            self.sem_full.acquire()  # Wait for a car to be available
            car = self.queue.get()
            print(f'Sold: {car.info()}')
            self.queue_stats[self.queue.size()] += 1  # Track queue size
            self.banana1.release()  # Signal that a slot is available
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))


def main():
    log = Log(show_terminal=True)

    # Create semaphores
    banana1 = threading.Semaphore(MAX_QUEUE_SIZE)  # Controls factory production
    sem_full = threading.Semaphore(0)  # Controls dealer sales

    # Create queue251 
    queue = Queue251()

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # Create factory and dealership threads
    factory = Factory(queue, banana1, sem_full)
    dealer = Dealer(queue, banana1, sem_full, queue_stats)

    log.start_timer()

    # Start factory and dealership threads
    factory.start()
    dealer.start()

    # Wait for factory and dealership to complete
    factory.join()
    dealer.join()

    log.stop_timer(f'All {sum(queue_stats)} cars have been created and sold.')

    xaxis = [i for i in range(0, MAX_QUEUE_SIZE)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count', filename='Production count vs queue size.png')


if __name__ == '__main__':
    main()
