"""
Author: Brother Keers + Claude 3 Sonnet

This example demonstrates cache thrashing and its performance impact.
"""

import time
import math
import sys
import multiprocessing as mp
import psutil
import random

def create_large_list(size):
    """Creates a large list of random integers to ensure cache thrashing."""
    return [random.randint(0, 2**32) for _ in range(size)]

def reverse_list_recursively_naive(lst, start=0, end=-1):
    """A poorly written algorithm that reverses the order of a list manually."""
    reversed_list = []
    for i in range(len(lst) - 1, -1, -1):
        reversed_list.append(lst[i])
    return reversed_list

def reverse_list_optimized(lst):
    """An optimized solution to reversing the order of a list using Python's built-in list slicing."""
    return lst[::-1]

def get_estimated_cache_size():
    """Returns an estimated size of the CPU cache in bytes."""
    total_memory = psutil.virtual_memory().total
    ram_based_estimate = int(total_memory * 0.01)  # Assuming cache size is 1% of total memory
    ram_based_estimate = int(ram_based_estimate / 10) # Reduce down further CHANGE OR REMOVE FOR TRUE PUNISHMENT!

    num_physical_cores = psutil.cpu_count(logical=False)
    cores_based_estimate = num_physical_cores * 256 * 1024  # Assuming 256 KB cache per core

    return ram_based_estimate, cores_based_estimate

def main():
    # Get estimated sizes of the CPU cache
    ram_based_estimate, cores_based_estimate = get_estimated_cache_size()
    print(f"RAM-based cache size estimate: {ram_based_estimate / (1024**2):.2f} MB")
    print(f"Cores-based cache size estimate: {cores_based_estimate / (1024**2):.2f} MB\n")

    list_size = 0
    while True:
        test_mode = input("Which test would you like to run:\n[1] Simple (Cores-based)\n[2] Punishing (RAM-based)\n")
        try:
            option = int(test_mode)
            if option == 1:
                list_size = min(ram_based_estimate, cores_based_estimate) * 2
            elif option == 2:
                list_size = max(ram_based_estimate, cores_based_estimate)
            else:
                print("Invalid option chosen! Please try again.")
                continue
            break
        except:
            print("Please enter only the number 1 or 2!")

    lst = create_large_list(list_size)
    print(f"Created list with {list_size:,} items ({list_size * 4 / (1024**2):.2f} MB)")

    # Optimized list reversal first
    start_time = time.time()
    reverse_list_optimized(lst)
    end_time = time.time()
    print(f"Optimized list reversal time: {end_time - start_time:.5f} secs")

    # Naive list reversal second
    start_time = time.time()
    reverse_list_recursively_naive(lst)
    end_time = time.time()
    print(f"Naive list reversal time: {end_time - start_time:.5f} secs")

if __name__ == "__main__":
    main()