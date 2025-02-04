import time
import threading
import random
from datetime import datetime
from cse251 import *

# Global Constants - DO NOT CHANGE
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

class Car():
    """ Represents a randomly generated car. """

    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        """ Initializes a new car with random attributes. """
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        time.sleep(random.random() / SLEEP_REDUCE_FACTOR)  # Simulate production delay
        print(f'Created: {self.info()}')  # Print car details

    def info(self):
        """ Returns a string representation of the car. """
        return f'{self.make} {self.model}, {self.year}'


class Queue251():
    """ Custom queue implementation for this assignment. """

    def __init__(self):
        self.__items = []

    def size(self):
        """ Returns the current queue size. """
        return len(self.__items)

    def put(self, item):
        """ Adds an item to the queue. """
        self.__items.append(item)

    def get(self):
        """ Removes and returns the front item from the queue. """
        return self.__items.pop(0)


class Factory(threading.Thread):
    """ Factory thread that creates cars and adds them to the queue. """

    def __init__(self, queue, banana1, banana2):
        threading.Thread.__init__(self)
        self.queue = queue
        self.banana1 = banana1
        self.banana2 = banana2

    def run(self):
        """ Produces cars and adds them to the queue. """
        for _ in range(CARS_TO_PRODUCE):
            self.banana1.acquire() 
            car = Car()
            self.queue.put(car) 
            self.banana2.release()

        
        self.banana1.acquire()
        self.queue.put(None)  
        self.banana2.release()


class Dealer(threading.Thread):
    """ Dealer thread that retrieves cars from the queue and sells them. """

    def __init__(self, queue, banana1, banana2, queue_stats):
        threading.Thread.__init__(self)
        self.queue = queue
        self.banana1 = banana1
        self.banana2 = banana2
        self.queue_stats = queue_stats

    def run(self):
        """ Sells cars and tracks queue stats. """
        while True:
            self.banana2.acquire()  #
            car = self.queue.get()  

            if car is None:  # Stop signal received
                break

            print(f'Sold: {car.info()}')
            
            if self.queue.size() < MAX_QUEUE_SIZE:
                self.queue_stats[self.queue.size()] += 1  # Track queue size

            self.banana1.release()  
            time.sleep(random.random() / SLEEP_REDUCE_FACTOR)  # Simulate selling delay


def main():
    """ Main function that sets up the factory and dealer. """
    log = Log(show_terminal=True)

    # Semaphores
    banana1 = threading.Semaphore(MAX_QUEUE_SIZE)  
    banana2 = threading.Semaphore(0)  

    # Shared queue
    queue = Queue251()
    queue_stats = [0] * MAX_QUEUE_SIZE  

    # Factory and dealer threads
    factory = Factory(queue, banana1, banana2)
    dealer = Dealer(queue, banana1, banana2, queue_stats)

    log.start_timer()

    factory.start()
    dealer.start()

    factory.join()
    dealer.join()

    log.stop_timer(f'All {sum(queue_stats)} cars have been created and sold.')

    # Graph queue stats
    xaxis = [i for i in range(MAX_QUEUE_SIZE)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', 
             x_label='Queue Size', y_label='Count', filename='Production_count_vs_queue_size.png')


if __name__ == '__main__':
    main()
