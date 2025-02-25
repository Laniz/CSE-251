import requests
import multiprocessing as mp
import time

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
    if is_prime(value):
        return f"{value:,} is prime"
    else:
        return f"{value:,} is not prime"
    
# Generate a smaller list of numbers to avoid excessive computation in this example
numbers = []

for i in range(1,1000000):
    numbers.append(i)



def main():
    start_timer = time.time()
    # Use multiprocessing Pool to parallelize the task_prime function
    pool_count = 4  # Use 2 processes as an example

    with mp.Pool(processes=pool_count) as pool:
        # map will apply the task_prime function to each element of numbers
        results = pool.map(task_prime, numbers)

    # Print the results from all processes
    
    # for result in results:
    #     print(result, flush=)

    end_timer = time.time()

    final_time = end_timer - start_timer

    print(f"This is the total runtime {final_time:4f}")

# Ensure that this script is executed only when run directly, not when imported
if __name__ == '__main__':
    main()
