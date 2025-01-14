# Lesson 10 Prepare: PThreads, MMap, and Shared Memory

Section | Content
--- | ---
1.1 | [Overview](#overview)
1.2 | [C and C++ Code](#c-and-c-code)
2   | [PThreads](#pthreads) :key:
2.1 | [Thread Classes](#threaded-classes) :key:
3   | [MMap (Memory Map)](#mmap-memory-map) :key:
4   | [Shared Memory](#shared-memory) :key:

:key: = Vital concepts that we will continue to build on in coming lessons / key learning outcomes for this course.

### Overview

So far in this course we have explored various aspects of threading and multiprocessing in Python programs. The concepts we have covered are transferable across other programming languages, but the implementation and syntax will differ. One major difference is Python's implementation of a global interpreter lock (GIL) which is not present in the larger part of programming languages. In this lesson we will explore lower-level parallelism and concurrency concepts that are language agnostic, meaning they should be present in any programming language that supports threading and multiprocessing.

### C and C++ Code

Our demonstration code for this week, and part of your assignments, will require C/C++. VS Code is capable of running (compiling and running) C/C++ code, but requires additional setup. You may use VS Code, or any other IDE, as long as you are capable of troubleshooting any issues yourself; your instructor will not have time to setup various environments within the short amount of time dedicated to these assignments.

If you do not have a C/C++ compiler already setup on your computer, **the recommended action is to setup free account at [replit.com](www.replit.com)**. Replit will allow you to write, compile, and run C/C++ programs in the browser. Replit supports many languages and is a good tool to invest your time in.

There are compilers that can be installed for C++ development.  CLion from [JetBrains.com](https://www.jetbrains.com/clion/) is a compiler that can run on Windows, Mac and Linux.  It is free for students.  Also, Windows has Visual Studio and Mac has XCode.

### PThreads

> POSIX Threads, usually referred to as pthreads, is an execution model that exists independently from a language, as well as a parallel execution model. It allows a program to control multiple different flows of work that overlap in time. Each flow of work is referred to as a thread, and creation and control over these flows is achieved by making calls to the POSIX Threads API.

To understand how pthreads work, we will be using them in the programming language C. PThreads also have locks and semaphores. The main difference is that they run in parallel instead of concurrently. There is no GIL here to limit threads.

You can see in the figure below that the threads on the right are sharing `code`, `data` and `files`.

![](./assets/shared_between_threads.png)

Example of PThreads. The difference between Python and PThreads is that when you create a thread using `pthread_create()`, it starts running immediately. There is still a `join()` function to bring the child thread back into the main or parent thread.

> NOTE: If you want to compile and run the following code examples and don't have a C compiler on your computer, you can use the website [repl.it](https://repl.it). It offers a free account for writing and running C programs. The free version of Visual Studio (for Windows) or XCode (for Mac) both can compile and run C programs.

```C
// https://www.geeksforgeeks.org/multithreading-c-2/

#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h>  // Header file for sleep()
#include <pthread.h> 
  
// A normal C function that is executed as a thread  
// when its name is specified in pthread_create() 
void *myThreadFun(void *vargp) 
{ 
    sleep(1); 
    printf("Printing from Thread \n"); 
    return NULL; 
} 
   
int main() 
{ 
    pthread_t thread_id; 
    printf("Before Thread\n"); 
    pthread_create(&thread_id, NULL, myThreadFun, NULL); 
    pthread_join(thread_id, NULL); 
    printf("After Thread\n"); 
    exit(0); 
}
```

Here is another example that contains 3 different uses for pthreads.

**example1()** This function create 1 thread and waits for it to finish.

**example2()** This example creates 10 threads and passes an integer as an argument. The integer is displaying to the console.

**example3()** This example shows how you can return values from a thread.

```c++
#include <iostream>
#include <cstdlib>
#include <pthread.h>

using namespace std;

// **************************************************************************
/* function to be run as a thread always must have the same signature:
   it has one void* parameter and returns void */
void *threadFunction1(void *arg)
{
    cout << "Hello, World!\n";
    return 0;
}

void example1()
{ 
    cout << "*************************\n";
    cout << "Example 1 - single thread\n";

    pthread_t thread;

    int createerror = pthread_create(&thread, NULL, threadFunction1, NULL);

    // creates a new thread with default attributes and NULL passed as the 
    // argument to the start routine
    if (!createerror) /*check whether the thread creation was successful*/
    {
        pthread_join(thread, NULL); /*wait until the created thread terminates*/
    }
    else
    {
        cout << "Error in creating thread\n";
    }

    cout << "Example 1 completed\n";
}

// **************************************************************************

void *threadFunction2(void *arg)
{
    cout << "I am thread #" << *(int *)arg << endl;
    return NULL;
}

void example2()
{
    cout << "*****************************\n";
    cout << "Example 2 - passing arguments\n";

    pthread_t threads[10];
    int ids[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    // Create 2 threads t1 and t2 with default attributes which will execute
    // function "thread_func()" in their own contexts with specified arguments.
    for (int i = 0; i < 10; ++i)
    {
        pthread_create(&threads[i], NULL, &threadFunction2, &ids[i]);
    }

    /* This makes the main thread wait on the death of t1 and t2. */
    for (int i = 0; i < 10; ++i)
    {
        pthread_join(threads[i], NULL);
    }

    cout << "Example 2 completed\n";
}

// **************************************************************************
struct thread_args
{
    int a;
    double b;
};

struct thread_result
{
    long x;
    double y;
};

void *thread_func(void *args_void)
{
    struct thread_args *args = (struct thread_args *)args_void;
    // The thread cannot return a pointer to a local variable
    struct thread_result *res = (struct thread_result *)malloc(sizeof *res);

    res->x  = 10 + args->a;
    res->y = args->a * args->b;
    return res;
}

void example3()
{
    cout << "*****************************************\n";
    cout << "Example 3 - returning values from threads\n";

    pthread_t threadL;
    struct thread_args in = { .a = 10, .b = 3.141592653 };
    void *out_void;
    struct thread_result *out;

    pthread_create(&threadL, NULL, thread_func, &in);
    pthread_join(threadL, &out_void);
    out = (struct thread_result *)out_void;
    cout << "out -> x = " << out->x << "\tout -> b = " << out->y << endl;
    free(out);

    cout << "Example 3 completed\n";
}

int main(void)
{
    example1();
    example2();
    example3();
}
```

Output:

```
*************************
Example 1 - single thread
Hello, World!
Example 1 completed
*****************************
Example 2 - passing arguments
I am thread #1
I am thread #2
I am thread #3
I am thread #4
I am thread #6
I am thread #5
I am thread #8
I am thread #9
I am thread #7
I am thread #10
Example 2 completed
*****************************************
Example 3 - returning values from threads
out -> x = 20   out -> b = 31.4159
Example 3 completed
```

### Threaded Classes

Using PThreads is a low level method of threading in C and C++.  Classes can also be used to add threads to a C++ program in the same method that Python has threaded classes.

#### Example 1 - hello world

The difference between Python threads and c++ threads, is that the c++ thread starts when created.

```c++
#include <iostream>
#include <thread>
using namespace std;

// Function to be executed by the thread
void hello_world() {
    cout << "Hello from thread!" << endl;
}

int main() {
    // Create a thread object and start it immediately
    // Note that hello_world is a pointer to the function.
    thread myThread(hello_world);  

    // Ensure the main thread waits for the new thread to finish
    myThread.join();  

    cout << "Hello from main!" << endl;
    return 0;
}
```

#### Example 2 - Passing arguments to a thread

This example has a string being passed to the thread.

```c++
#include <iostream>
#include <thread>
#include <string>
#include <vector>

using namespace std;

// Function to be executed by the thread
void processData(const string& threadName) {
    cout << "Thread '" << threadName << "' received data: ";
}

int main() {
    // Create and start threads with different names
    thread thread1(processData, "Thread 1"); 
    thread thread2(processData, "Thread 2"); 

    // Wait for threads to finish
    thread1.join();
    thread2.join();

    cout << "Main thread finished." << endl;
    return 0;
}
```

#### Example 3 - using a barrier

This example had 4 threads and 1 barrier.  The threads will wait on the barrier until they are all finished.

```c++
#include <iostream>
#include <thread>
#include <vector>
#include <barrier>  // For std::barrier (C++20)
using namespace std;

// Function representing work each thread performs
void worker(barrier<>& barrier, int threadId) {
    cout << "Thread " << threadId << ": Doing some work..." << endl;

    this_thread::sleep_for(chrono::milliseconds(500 + (threadId * 100)));

    cout << "Thread " << threadId << ": Reached barrier, waiting for others..." << endl;

    barrier.arrive_and_wait();

    cout << "Thread " << threadId << ": All threads arrived! Continuing..." << endl;
}

int main() {
    const int numThreads = 4;

    barrier syncBarrier(numThreads);

    vector<thread> threads;
    for (int i = 0; i < numThreads; ++i) {
        threads.emplace_back(worker, ref(syncBarrier), i);
    }

    for (auto& thread : threads) {
        thread.join();
    }

    cout << "All threads finished!" << endl;
    return 0;
}
```

#### Example 4 - using a lock

This program will update a global variable using a lock to stop a race condition.

```c++
#include <iostream>
#include <thread>
#include <mutex>
using namespace std;

mutex counterMutex;  // Global mutex to protect the counter
int counter = 0; 

void incrementCounter(int numIncrements) {
    for (int i = 0; i < numIncrements; ++i) {
        // Lock the mutex before accessing the counter
        lock_guard<mutex> lock(counterMutex); 
        ++counter;
        cout << "Thread ID: " << this_thread::get_id() << ", Counter: " << counter << endl;
    }
}

int main() {
    // Create two threads
    thread thread1(incrementCounter, 1000);
    thread thread2(incrementCounter, 1000);

    // Wait for the threads to finish
    thread1.join();
    thread2.join();

    cout << "Final Counter: " << counter << endl;
    return 0;
}
```

### MMap (Memory Map)

[Python Documentation on MMap](https://docs.python.org/3/library/mmap.html)

What is MMap?

>  It is a method of memory-mapped file I/O. It implements demand paging because file contents are not read from disk directly and initially do not use physical RAM at all. The actual reads from disk are performed in a "lazy" manner, after a specific location is accessed. 

Memory mapping is used for speed. The operating system will "map" a file to a memory. You can then access the contents of the file just by access that memory. If your program makes a change in the memory, the OS will ensure that the change is written back to the file when the file is unmapped.

Memory mapping can also be used to share memory between processes on the same computer.

**Example 1**

Example of mapping a file to memory and then displaying the contents of the file by accessing that memory. In this program, we need to open the file first and then map it to memory. Once mapped to memory, we can get to the contents of the file. The `mmap` object `map_file` has methods that can be used to access it.

Contents of **data.txt**

```
111111111
222222222
333333333
444444444
555555555
666666666
777777777
888888888
999999999
000000000
```

This program will open the `data.txt` file and read it line by line.

```python
# https://realpython.com/python-mmap/#search-a-memory-mapped-file

import mmap

def mmap_io_display_lines(filename):
    with open(filename, mode="r", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as map_file:
            for line in iter(map_file.readline, b""):
                print(line)

def main():
    mmap_io_display_lines('data.txt')

if __name__ == '__main__':
    main()
```

Output from above's program. Notice that we are dealing with binary strings denoted with the "b" before the string. Also, the "\r" and "\n" are part of the output. This is because in Windows, each text line ends with a carriage return "\r" and a new line "\n".

```
b'111111111\r\n'
b'222222222\r\n'
b'333333333\r\n'
b'444444444\r\n'
b'555555555\r\n'
b'666666666\r\n'
b'777777777\r\n'
b'888888888\r\n'
b'999999999\r\n'
b'000000000'    
```

**Example 2**

In the example, the program will read each character of the file and print it to the console. It will be using the `read_byte()` method for this.

```python
# https://realpython.com/python-mmap/#search-a-memory-mapped-file

import mmap

def mmap_io(filename):
    with open(filename, mode="r", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as map_file:
            for i in range(map_file.size()):
                print(chr(map_file.read_byte()), end='')

def main():
    mmap_io('data.txt')

if __name__ == '__main__':
    main()
```

Output:

```
111111111
222222222
333333333
444444444
555555555
666666666
777777777
888888888
999999999
000000000
```

The above program can be changed from using the method `read_byte()` to using `[]` notation

```python
import mmap

def mmap_io(filename):
    with open(filename, mode="r", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as map_file:
            for i in range(map_file.size()):
                print(chr(map_file[i]), end='')

def main():
    mmap_io('data.txt')

if __name__ == '__main__':
    main()
```

**Example 3**

I create a text file with 10,000,000 lines. The file size was 877 Mb. There are two Python programs where they will count the lines of this large file. The first program will use mmap to read the file and the other normal file processing statements.

Program using MMap

```Python
import mmap
import time

def mmap_count_lines(filename):
    count = 0
    with open(filename, mode="r", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as map_file:
            for line in iter(map_file.readline, b""):
                count += 1
    return count

def main():
    start = time.perf_counter()
    count = mmap_count_lines('large.txt')
    end = time.perf_counter()
    print(f'{count} lines processed, {end - start}')

if __name__ == '__main__':
    main()
```

Program using normal file statements

```Python
import time

def count_lines(filename):
    count = 0
    with open(filename, mode="r", encoding="utf8") as file_obj:
        for line in file_obj:
            count += 1
    return count

def main():
    start = time.perf_counter()
    count = count_lines('large.txt')
    end = time.perf_counter()
    print(f'{count} lines processed, {end - start}')

if __name__ == '__main__':
    main()
```

Output from both programs:

```
python speed_mmap.py
10000000 lines processed, 1.1074841

python speed_normal.py
10000000 lines processed, 3.0482346000000002
```

The mmap version was about 3 times faster in reading the text file. One of the reasons for this speed increase is that access to the memory in a mmap doesn't require a system call to the operating system for data. One system call to create the mmap and another to unmap/close it.

Also, you can write to a mmap. There are many examples on the Internet that show how to do this.

**Example 4**

You can use the MMap as a string and to change it. Notice the file mode used in the open() function.

```python
import mmap

def mmap_io(filename):
    with open(filename, mode="r+", encoding="utf8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as mmap_obj:

            # Print the first 10 characters
            print(mmap_obj[:10])
            print()

            # Print the last 10 characters
            print(mmap_obj[-10:])
            print()

            # Print the characters between 15 and 25
            print(mmap_obj[15:25])

            # Change 9th character to the letter 'a'
            mmap_obj[8] = 97


def main():
    mmap_io('data.txt')

if __name__ == '__main__':
    main()

```

Output:

```
b'111111111\r'

b'\n000000000'

b'22222\r\n333'
```

### Shared Memory

When we create processes in Python, the process will make a copy of the Python program and run in with it's own GIL. We already know we can use a manager to create a variable or array that we can share between them, but we can not use MMap directly between processes because MMap objects can not be pickled.

There is another package in Python's `multiprocessing` package called `shared_memory` that we can use instead. Please review the [Python Documentation on shared_memory](https://docs.python.org/3/library/multiprocessing.shared_memory.html).

**Example 1**

Creating a shared list. The method ShareableList() can be used to create a shared list. This list works the same as the normal Python list except that once created, it can not shrink or grow. 


```python
from multiprocessing import shared_memory
import multiprocessing as mp

def do_work(shared_name, value, start, end):
    # Attach to an exist shared memory block
    shared = shared_memory.SharedMemory(shared_name)
    for i in range(start, end):
        shared.buf[i] = value
    # need to close this local shared memory block access
    shared.close()
    

def main():
    shared = shared_memory.SharedMemory(create=True, size=100)
    # Create a shared memory block of 100 items
    print(f'Shared memory name = {shared.name}')

    # Divide the work among two processes, storing partial results in "shared"
    p1 = mp.Process(target=do_work, args=(shared.name, 1, 0, 50))
    p2 = mp.Process(target=do_work, args=(shared.name, 2, 50, 100))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    # we must loop through the shared.buf array to display the values
    print('Buffer values:')
    for i in range(100):
        print(shared.buf[i], end=' ')
    print()

    # close and give the memory block back to the OS
    shared.close()
    shared.unlink()

if __name__ == '__main__':
    main()
```

output of a few runs of the above program. Notice that every shared memory variable has an assigned name given to it. You can assign your own name. If you don't, a random name is assigned.

```
Shared memory name = wnsm_e0878435
Buffer values:
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 


Shared memory name = wnsm_ae137812
Buffer values:
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 


Shared memory name = wnsm_be564f73
Buffer values:
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 

```

**Example 2**

Here is the above code example using shared list names between processes.

```python
from multiprocessing import shared_memory
import multiprocessing as mp

def do_work(shared, value, start, end):
    for i in range(start, end):
        shared[i] = value
    

def main():
    # Create a shared memory block of 100 items
    shared = shared_memory.ShareableList([0] * 100)

    # Divide the work among two processes, storing partial results in "shared"
    p1 = mp.Process(target=do_work, args=(shared, 1, 0, 50))
    p2 = mp.Process(target=do_work, args=(shared, 2, 50, 100))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    # we must loop through the shared.buf array to display the values
    print('Buffer values:')
    for i in range(100):
        print(shared[i], end=' ')
    print()

if __name__ == '__main__':
    main()
```    

output:

```
Buffer values:
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 2 2 
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
```