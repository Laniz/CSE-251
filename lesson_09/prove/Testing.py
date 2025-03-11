# import multiprocessing as mp

# def fibonacci(n):
#     if n == 0:
#         return 0
#     elif n == 1:
#         return 1
#     return fibonacci(n - 1) + fibonacci(n - 2)

# if __name__ == '__main__':
#     n_values = range(10)  # An iterable of numbers from 0 to 9

#     with mp.Pool() as pool:
#         results = pool.map(fibonacci, n_values)
#     print(results) # Output will be a list of Fibonacci numbers for 0, 1, 2, ..., 9


def fun2(n):
    if n==0:
        return 1
    return n**3 + fun2(n-1)

if __name__ == '__main__':
    print(fun2(10))