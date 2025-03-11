"""
Course: CSE 251 
Lesson: L09 Prove Part 2
File:   prove_part_2.py
Author: Shepherd Ncube

Purpose: Part 2 of prove 9, finding the path to the end of a maze using recursion.

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- You MUST use recursive threading to find the end of the maze.
- Each thread MUST have a different color than the previous thread:
    - Use get_color() to get the color for each thread; you will eventually have duplicated colors.
    - Keep using the same color for each branch that a thread is exploring.
    - When you hit an intersection spin off new threads for each option and give them their own colors.

This code is not interested in tracking the path to the end position. Once you have completed this
program however, describe how you could alter the program to display the found path to the exit
position:

What would be your strategy?

I would use a tree structure where each node represents a position in the maze. The root node would be the starting position, and each new position would be added as a child node to its parent. When a thread explores a new position, it creates a new child node and links it to the current node. Once a thread reaches the exit, we can trace the path back to the root by following the parent-child links.

I learnt about trees in my CSE 212 class, which I am taking at the same time as this class.

Why would it work?

The tree naturally records how each position was reached, and when the exit is found, the correct path can be extracted by following the parent nodes back to the start. Since each thread only moves forward, the tree structure efficiently maintains the path without interfering with the concurrent nature of the program.


"""


import math
import threading
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 700
COLOR = (0, 0, 255)
COLORS = (
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (128, 0, 0),
    (128, 128, 0),
    (0, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (0, 0, 128),
    (72, 61, 139),
    (143, 143, 188),
    (226, 138, 43),
    (128, 114, 250)
)
SLOW_SPEED = 100
FAST_SPEED = 0

# Globals
current_color_index = 0
thread_count = 0
stop = False
speed = SLOW_SPEED

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color


# TODO: Add any function(s) you need, if any, here.

#locks
color_lock = threading.Lock()  
count_lock = threading.Lock() 
visited_lock = threading.Lock() 
visited = set()  


def solve_find_end(maze):
    global stop, thread_count, visited
    start = maze.get_start_pos()
    stop_event = threading.Event()
    visited = set()  

    def solve_find_end(maze):
        global stop, thread_count, visited
        start = maze.get_start_pos()
        stop_event = threading.Event()
        visited = set()  

    def explore(x, y, color, maze):
        global stop, thread_count
        if stop_event.is_set():  
            return False

        with visited_lock:
            if (x, y) in visited:
                return False
            visited.add((x, y))

        if not maze.can_move_here(x, y):  
            return False
        if maze.at_end(x, y): 
            maze.move(x, y, color)
            stop_event.set() 
            return True

        maze.move(x, y, color)

        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        valid = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if maze.can_move_here(nx, ny):
                valid.append((dx, dy))

        if len(valid) == 0:
            return False 

        threads = []
        if len(valid) > 1:
            for dx, dy in valid[1:]:
                with color_lock:
                    new_color = get_color() 
                with count_lock:
                    thread_count += 1 
                thread = threading.Thread(target=explore, args=(x + dx, y + dy, new_color, maze))
                thread.start()
                threads.append(thread)

        
            found = explore(x + valid[0][0], y + valid[0][1], color, maze)

        
            for thread in threads:
                thread.join()
            return found
        else:
            return explore(x + valid[0][0], y + valid[0][1], color, maze)

    with count_lock:
        thread_count += 1


    with color_lock:
        color = get_color()
    explore(*start, color, maze)



def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count
    global speed

    # Create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    while not done:
        if screen.play_commands(speed):
            key = cv2.waitKey(0)
            if key == ord('1'):
                speed = SLOW_SPEED
            elif key == ord('2'):
                speed = FAST_SPEED
            elif key == ord('q'):
                exit()
            elif key != ord('p'):
                done = True
        else:
            done = True


def find_ends(log):
    """ Do not change this function """

    files = (
        ('very-small.bmp', True),
        ('very-small-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False),
        ('large-squares.bmp', False),
        ('large-open.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        filename = f'./mazes/{filename}'
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)


if __name__ == "__main__":
    main()