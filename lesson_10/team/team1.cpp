/*
 * CSE 251, Week 10
 * Team 1 - finding primes in an array
 *
 * NOTE: You are using the thread class, NOT PThreads!!!!!!!
 *
 * TODO
 * 1) Get this program compiling an running in a compiler or replit.com
 * 2) Create a thread to process the array
 * 3) Create multiple threads to process the array
 * 4) if the output of the primes from the threads are mixed up, add a lock for
 *    the cout statements.
 */

#include <iostream>
#include <thread>
#include <mutex>

using namespace std;

#define NUMBERS 500

mutex counterLock; // lock for primes
int primes = 0;    // Global count

// ----------------------------------------------------------------------------
int isPrime(int number)
{
    if (number <= 3 && number > 1)
    {
        return 1; // as 2 and 3 are prime
    }
    else if (number % 2 == 0 || number % 3 == 0)
    {
        return 0; // check if number is divisible by 2 or 3
    }
    else
    {
        for (unsigned int i = 5; i * i <= number; i += 6)
        {
            if (number % i == 0 || number % (i + 2) == 0)
                return 0;
        }
        return 1;
    }
}

int main()
{

    srand(42);

    // Create the array of numbers and assign random values to them
    int *arrayValues = new int[NUMBERS];
    for (int i = 0; i < NUMBERS; i++)
    {
        arrayValues[i] = rand() % 1000000000;
        //        cout << arrayValues[i] << ", ";
    }
    cout << endl;

    cout << endl
         << "Starting findPrimes" << endl;
    // Loop through the array looking for prime numbers
    int start = 0;
    int end = NUMBERS - 1;
    for (int i = start; i < end; i++)
    {
        if (isPrime(arrayValues[i]) == 1)
        {
            lock_guard<mutex> lock(counterLock);
            ++primes;
            cout << arrayValues[i] << endl;
        }
    }

    // Should be the same each run of the program
    cout << "\nPrimes found: " << primes << endl;

    delete[] arrayValues;
    return 0;
}
