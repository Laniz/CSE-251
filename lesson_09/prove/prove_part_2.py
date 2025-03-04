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


# Thread-safe locks
color_lock = threading.Lock()  # Single lock for color operations
count_lock = threading.Lock()  # Lock for thread count
visited_lock = threading.Lock()  # Lock for visited positions
visited = set()  # Track visited positions to avoid loops


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
        if maze.at_end(x, y):  # If exit found, mark it and stop
            maze.move(x, y, color)
            stop_event.set()  # Signal that we've found the exit
            return True

        maze.move(x, y, color)

        # Check all valid directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        valid = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if maze.can_move_here(nx, ny):
                valid.append((dx, dy))

        if len(valid) == 0:
            return False  # Dead end

        threads = []
        if len(valid) > 1:
            for dx, dy in valid[1:]:
                with color_lock:
                    new_color = get_color()  # Get a new color for each new thread
                with count_lock:
                    thread_count += 1  # Increment thread count
                thread = threading.Thread(target=explore, args=(x + dx, y + dy, new_color, maze))
                thread.start()
                threads.append(thread)

            # Continue with the first direction (same color)
            found = explore(x + valid[0][0], y + valid[0][1], color, maze)

            # Wait for all threads to finish before returning
            for thread in threads:
                thread.join()
            return found
        else:
            # Only one valid direction, explore in the same thread
            return explore(x + valid[0][0], y + valid[0][1], color, maze)

    # Start the exploration with the initial color
    with color_lock:
        color = get_color()
    explore(*start, color, maze)  # Pass `maze` explicitly



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