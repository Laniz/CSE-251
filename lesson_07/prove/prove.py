"""
Course: CSE 251 
Lesson: L07 Prove
File:   prove.py
Author: <Add name here>

Purpose: Process Task Files.

Instructions:

See Canvas for the full instructions for this assignment. You will need to complete the TODO comment
below before submitting this file:

Note: each of the 5 task functions need to return a string.  They should not print anything.

TODO:
"""

'''
I only have 8 cores on my computer, and here is how I decided to split them: 
Using all 8 cores actually slowed the run time by 2 seconds. I then decided to prioritize the most CPU-dependent tasks, leaving everything else on 1 core. 
I also left all tasks that are I/O-bound on 1 core, as they cannot be sped up by using more processes
Prime checking (CPU bound and heavy) = 2
Word search (I/O-bound) = 1
Uppercase conversion (Cpu bound, but not heavy) = 1
Summation (CPU bound and heavy) = 2
Web requests (I/O-bound) = 1
'''

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Don't change
from cse251 import *

# Constants - Don't change
TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# TODO: Change the pool sizes and explain your reasoning in the header comment


PRIME_POOL_SIZE = 2
WORD_POOL_SIZE  = 1
UPPER_POOL_SIZE = 1
SUM_POOL_SIZE   = 2
NAME_POOL_SIZE  = 1

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    if is_prime(value) == True:
        # result_primes.append(f"{value:,} is prime")
        pre_results = f"{value:,} is prime"
        return pre_results
    else:
        # result_primes.append(f"{value:,} is not prime")
        pre_results_2 = f"{value:,} is not prime"
        return pre_results_2


def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open('words.txt') as f:
        if word in f.read():
            # result_words.append(f"{word} Found")
            pre_results = f"{word} Found"
            return(pre_results)
        else:
            # result_words.append(f"{word} not found")
            pre_results_2 = f"{word} not found"
            return(pre_results_2)


def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    stripped_text = text.strip()
    upper_case = stripped_text.upper()
    # result_upper.append(f"{stripped_text} ==> {upper_case}")
    pre_results = f"{stripped_text} ==> {upper_case}"
    return(pre_results)


def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of all numbers between start_value and end_value
        answer = {start_value:,} to {end_value:,} = {total:,}
    """
    list_of_numbers = []
    for i in range(start_value, end_value):
        list_of_numbers.append(i)
    
    total = sum(list_of_numbers)
    # result_sums.append(f"sum of {start_value:,} to {end_value:,} = {total:,}")
    pre_results = f"sum of {start_value:,} to {end_value:,} = {total:,}"
    return(pre_results)


def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    url1 = url
    url_2 = f"{url1}"
    response = requests.get(url_2)
    data = response.json()

    if response.status_code != 200:
        # result_names.append(f"{url_2} had an error receiving the information")
        pre_results = f"{url_2} had an error receiving the information"
        return(pre_results)
    else:
        name = data["name"]
        # result_names.append(f"{url_2} has name {name}")
        pre_results_2 = f"{url_2} has name {name}"
        return(pre_results_2)

    
def collect_result(result_list, result):
    """Callback function to append results to the global list."""
    result_list.append(result)

def main():
    log = Log(show_terminal=True)
    log.start_timer()

    count = 0
    with mp.Pool(processes=PRIME_POOL_SIZE) as prime_pool, \
         mp.Pool(processes=WORD_POOL_SIZE) as word_pool, \
         mp.Pool(processes=UPPER_POOL_SIZE) as upper_pool, \
         mp.Pool(processes=SUM_POOL_SIZE) as sum_pool, \
         mp.Pool(processes=NAME_POOL_SIZE) as name_pool:

        task_files = glob.glob("tasks/*.task")
        for filename in task_files:
            task = load_json_file(filename)
            count += 1
            task_type = task['task']

            if task_type == TYPE_PRIME:
                prime_pool.apply_async(task_prime, args=(task['value'],), callback=lambda res: collect_result(result_primes, res))
            elif task_type == TYPE_WORD:
                word_pool.apply_async(task_word, args=(task['word'],), callback=lambda res: collect_result(result_words, res))
            elif task_type == TYPE_UPPER:
                upper_pool.apply_async(task_upper, args=(task['text'],), callback=lambda res: collect_result(result_upper, res))
            elif task_type == TYPE_SUM:
                sum_pool.apply_async(task_sum, args=(task['start'], task['end']), callback=lambda res: collect_result(result_sums, res))
            elif task_type == TYPE_NAME:
                name_pool.apply_async(task_name, args=(task['url'],), callback=lambda res: collect_result(result_names, res))
            else:
                log.write(f'Error: unknown task type {task_type}')

        # Wait on the pools  
        prime_pool.close()
        word_pool.close()
        upper_pool.close()
        sum_pool.close()
        name_pool.close()

        prime_pool.join()
        word_pool.join()
        upper_pool.join()
        sum_pool.join()
        name_pool.join()  

    # DO NOT change any code below this line!
    #---------------------------------------------------------------------------

    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Total time to process {count} tasks')


if __name__ == '__main__':
    main()
