"""
Course: CSE 251 
Lesson: L06 Prove
File:   prove.py
Author: shepherd ncube

Purpose: Processing Plant

Instructions:
- Implement the necessary classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
from datetime import datetime  # Corrected import

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.json'
BOXES_FILENAME = 'boxes.txt'

# Settings constants
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ Bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """
    Gift of a large marble and a bag of marbles - Don't change

    Parameters:
        large_marble (string): The name of the large marble for this gift.
        marbles (Bag): A completed bag of small marbles for this gift.
    """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'

class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver',
              'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda',
              'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green',
              'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange',
              'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink',
              'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple',
              'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango',
              'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink',
              'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green',
              'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple',
              'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue',
              'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue',
              'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow',
              'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink',
              'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink',
              'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
              'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue',
              'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, send_to_bagger, marble_count, delay):
        mp.Process.__init__(self)
        self.send_to_bagger = send_to_bagger
        self.marble_count = marble_count
        self.delay = delay

    def run(self):
        for _ in range(self.marble_count):
            marble = random.choice(Marble_Creator.colors)
            self.send_to_bagger.send(marble)  
            time.sleep(self.delay)
        self.send_to_bagger.send(None) 
        self.send_to_bagger.close()  

class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """

    def __init__(self, send_to_assembler, receive_from_creator, bag_size, delay):
        mp.Process.__init__(self)
        self.send_to_assembler = send_to_assembler
        self.receive_from_creator = receive_from_creator
        self.bag_size = bag_size
        self.delay = delay

    def run(self):
        bag = Bag()
        while True:
            marble = self.receive_from_creator.recv() 
            if marble is None:
                # if bag.get_size() > 0:
                    # self.send_to_assembler.send(bag) 
                break
            bag.add(marble)
            if bag.get_size() == self.bag_size:
                self.send_to_assembler.send(bag) 
                bag = Bag() 
                time.sleep(self.delay)
        self.send_to_assembler.send(None)  
        self.receive_from_creator.close()
        self.send_to_assembler.close()

class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """

    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, receive_from_bagger, send_to_wrapper, delay):
        mp.Process.__init__(self)
        self.receive_from_bagger = receive_from_bagger
        self.send_to_wrapper = send_to_wrapper
        self.delay = delay

    def run(self):
        while True:
            bag = self.receive_from_bagger.recv() 
            if bag is None:
                self.send_to_wrapper.send(None)  
                break
            large_marble = random.choice(Assembler.marble_names)
            gift = Gift(large_marble, bag)
            self.send_to_wrapper.send(gift)  
            time.sleep(self.delay)
        self.receive_from_bagger.close()
        self.send_to_wrapper.close()

class Wrapper(mp.Process):
    """ Takes created gifts and "wraps" them by placing them in the boxes file. """

    def __init__(self, receive_from_assembler, delay, gift_count):
        mp.Process.__init__(self)
        self.receive_from_assembler = receive_from_assembler
        self.delay = delay
        self.gift_count = gift_count 

    def run(self):
        with open(BOXES_FILENAME, "w") as file:  
            while True:
                gift = self.receive_from_assembler.recv()  
                if gift is None:
                    break
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
                file.write(f"[{timestamp}] {gift}\n")  
                time.sleep(self.delay)
                with self.gift_count.get_lock(): 
                    self.gift_count.value += 1
        self.receive_from_assembler.close()

def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')

def main():
    """ Main function """

    log = Log(show_terminal=True)
    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}')
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    # Create Pipes
    creator_to_bagger, bagger_recv = mp.Pipe()
    bagger_to_assembler, assembler_recv = mp.Pipe()
    assembler_to_wrapper, wrapper_recv = mp.Pipe()

    # Shared counter for gifts
    gift_count = mp.Value('i', 0)

    # Delete final boxes file if it exists
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

   
    log.write('Create the processes')
    marble_count = settings[MARBLE_COUNT]
    creator_delay = settings[CREATOR_DELAY]
    bag_size = settings[NUMBER_OF_MARBLES_IN_A_BAG]
    bagger_delay = settings[BAGGER_DELAY]
    assembler_delay = settings[ASSEMBLER_DELAY]
    wrapper_delay = settings[WRAPPER_DELAY]

    # Create processes
    creator = Marble_Creator(creator_to_bagger, marble_count, creator_delay)
    bagger = Bagger(bagger_to_assembler, bagger_recv, bag_size, bagger_delay)
    assembler = Assembler(assembler_recv, assembler_to_wrapper, assembler_delay)  
    wrapper = Wrapper(wrapper_recv, wrapper_delay, gift_count)

    log.write('Starting the processes')
    creator.start()
    bagger.start()
    assembler.start()
    wrapper.start()

    log.write('Waiting for processes to finish')
    creator.join()
    bagger.join()
    assembler.join()
    wrapper.join()

    # Close unused pipe ends
    creator_to_bagger.close()
    bagger_recv.close()
    bagger_to_assembler.close()
    assembler_recv.close()
    assembler_to_wrapper.close()
    wrapper_recv.close()

    # Display final boxes and log gift count
    display_final_boxes(BOXES_FILENAME, log)
    log.write(f'Total gifts created: {gift_count.value}')

    log.stop_timer(f'Total time')

if __name__ == '__main__':
    main()