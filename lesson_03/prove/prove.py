"""
Course: CSE 251 
Lesson: L03 Prove
File:   prove.py
Author: <Add name here>

Purpose: Video Frame Processing

Instructions:

- Follow the instructions found in Canvas for this assignment.
- No other packages or modules are allowed to be used in this assignment.
  Do not change any of the from and import statements.
- Only process the given MP4 files for this assignment.
- Do not forget to complete any TODO comments.
"""

from matplotlib.pylab import plt  # load plot library
from setup import setup as ensure_assignment_is_setup
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# 4 more than the number of cpu's on your computer
total_cpu_count = 12

# TODO Your final video needs to have 300 processed frames.
# However, while you are testing your code, set this much lower!
FRAME_COUNT = 300

# RGB values for reference
RED = 0
GREEN = 1
BLUE = 2


def create_new_frame(args):
    """
    Creates a new image file from image_file and green_file.
    Parameters:
        args (tuple): Contains the image file, green screen file, and output file path.
    """
    image_file, green_file, process_file = args

    # this print() statement is there to help see which frame is being processed
    print(f'{process_file[-7:-4]}', end=',', flush=True)

    image_img = Image.open(image_file)
    green_img = Image.open(green_file)

    # Make Numpy array
    np_img = np.array(green_img)

    # Mask pixels
    mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

    # Create mask image
    mask_img = Image.fromarray((mask * 255).astype(np.uint8))

    image_new = Image.composite(image_img, green_img, mask_img)
    image_new.save(process_file)


def main():
    all_process_time = timeit.default_timer()
    log = Log(show_terminal=True)

    xaxis_cpus = []
    yaxis_times = []

    # Process all frames trying 1 CPU, then 2, up to total_cpu_count
    for total_cpu_count in range(1, total_cpu_count + 1):
        print(f"\nProcessing with {total_cpu_count} CPU(s)...")
        xaxis_cpus.append(total_cpu_count)

        # Prepare arguments for all frames
        frame_processor = [
            (
                f'elephant/image{image_number:03d}.png',
                f'green/image{image_number:03d}.png',
                f'processed/image{image_number:03d}.png',
            )
            for image_number in range(1, FRAME_COUNT + 1)
        ]

        # Process frames using multiprocessing
        start_time = timeit.default_timer()
        with mp.Pool(total_cpu_count) as pool:
            pool.map(create_new_frame, frame_processor)
        elapsed_time = timeit.default_timer() - start_time
        yaxis_times.append(elapsed_time)

        # Log the time taken
        log.write(f'Time for {FRAME_COUNT} frames using {total_cpu_count} process(es): {elapsed_time:.6f} seconds')

    # Log the total time this took
    log.write(f'Total Time for ALL processing: {timeit.default_timer() - all_process_time}')

    # Create plot of results and save it to a PNG file
    plt.plot(xaxis_cpus, yaxis_times, marker='o', label=f'{FRAME_COUNT} frames')
    
    plt.title('Processing Time vs CPU Cores')
    plt.xlabel('CPU Cores')
    plt.ylabel('Seconds')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig(f'plot_{FRAME_COUNT}_frames.png')
    plt.show()


if __name__ == "__main__":
    ensure_assignment_is_setup()
    main()
