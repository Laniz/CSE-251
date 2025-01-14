# Lesson 2 Prepare: Class Threads and Communication

Section | Content
--- | ---
1   | [Overview](#overview)
2   | [States of a Thread](#states-of-a-thread) :key:
2.1 | [I/O Bound and CPU Bound Code](#io-bound-and-cpu-bound-code)
3   | [Thread Objects](#thread-objects)
3.1 | [What is shared between Threads?](#what-is-shared-between-threads) :key:
3.2 | [Thread Safe](#thread-safe) :key:
4   | [Race Conditions](#race-conditions) :key:
5   | [Deadlock](#deadlock) :key:
6   | [Synchronization Tools](#synchronization-tools) :key:

:key: = Vital concepts that we will continue to build on in coming lessons / key learning outcomes for this course.

### Overview

Last lesson we learned to create threads that are considered *stand alone* or independent. This means that when a thread is running, it doesn't effect other threads and there was no communication between threads. In this lesson we are going to learn about the communication tools that allow threads to work together.

### States of a Thread

The operating system (Windows, Mac, Linux, etc.) is in control of managing threads. The following diagram outlines the different states of a thread.

![](assets/process-states.png)

**Created**

When a thread is first started, it is in the created state. This is where the operating system creates (reserves) the thread's memory and resources for managing the thread.

**Waiting**

This state is where the thread is waiting to run on the computer's CPU. There can be many threads in this state and they are waiting in a queue.

**Running**

This is the state where the thread is running on a CPU. There are three ways that a thread can be removed from this state:

1. The thread finishes its task. If this happens the thread goes into the `terminated` state.
2. The thread makes an I/O (input / output) call. Examples of I/O calls are reading/writing to a file, making a request over the internet, printing to a terminal window, and so on. Because these I/O calls take time, that thread is placed on the blocked queue and has state of `blocked`.
3. Each thread is given only a short amount of time, called a time slice, to run on the CPU. If the time slice a thread was given runs out, the thread is paused and placed back on the waiting queue to be run again shortly. Waiting threads will wait and run in turn.

**Blocked**

Here the thread is waiting for an I/O request to be completed. When the operating system completes the I/O request, that thread is moved to the waiting queue.

**Terminated**

When the thread is finished, it moves to the terminated state. Here the operating system can free any resources used by the thread.

### I/O Bound and CPU Bound Code

Remember that we can write code to run in parallel or concurrently depending on the type of problem we are trying to solve. Here is what that looks like from a threads perspective:

- I/O bound code will cycle between `running` -> `blocked` -> `waiting` states.
- CPU bound code will bounce between `running` and `waiting` states.

## Thread Objects

Python allows the creation of threaded classes. Instead of just having a function that is a thread, a threaded class allows for more complex code. You should watch a [review of classes in Python](https://www.youtube.com/watch?v=ZDa-Z5JzLYM).

There are two methods that you **must** implement for a threaded class; of course you can create others if you need them.

**`__init__()`**

This method is used to initialize the instance of the object you just created and to call the parent class' constructor. You are free to add any number of arguments that you require. This method needs to call the parent or super class's `__init__` method.

**`run()`**

After you create an instance of this class, when you call the `start()` method, the `run()` method will be executed. The only method this argument has is `self`. When the `run()` method exits, then the thread is finished. Within the `run()` method, you can call other methods in your class if you have them.

```python
import threading

class Display_Hello(threading.Thread):

    # constructor
    def __init__(self, number, message):
        # calling parent class constructor
        super().__init__()

        # Create or assign any variables that you need
        self.number = number
        self.message = message
    
    # This is the method that is run when start() is called
    def run(self):
        time.sleep(self.number)
        print(f'Message: {self.message}')
    

if __name__ == '__main__':
    # This is how to create the thread object -> name of the class and arguments for __init__()
	hello1 = Display_Hello(1, 'Hello from thread 1')
	hello2 = Display_Hello(2, 'Hello from thread 2')

    # Start still needs to be called.  This will call the run() method in the object.
	hello1.start()
	hello2.start()

    # Wait for them to finish
	hello1.join()
	hello2.join()
```

**Output:**

```text
Message: Hello from thread 1
Message: Hello from thread 2
```

Here is an example of a threaded class *returning* a value; we simply access the classes property after the thread is finished. Any variables (properties) in the instance object can be accessed.

```python
import threading

class Add_Two(threading.Thread):

    # constructor
    def __init__(self, number):
        # calling parent class constructor
        threading.Thread.__init__(self)
        self.number = number
    
    # This is the method that is run when start() is called
    def run(self):
    	# Create a new variable to hold the answer/results
    	# This variable is public and can be used in the
    	# main function.
    	self.results = self.number + 2
   

if __name__ == '__main__':
	add1 = Add_Two(100)
	add2 = Add_Two(200)

	add1.start()
	add2.start()

	add1.join()
	add2.join()

	print(f'Add_Two(100) returns {add1.results}')
	print(f'Add_Two(200) returns {add2.results}')

```

Output:

```text
Add_Two(100) returns 102
Add_Two(200) returns 202
```

### What is shared between Threads?

You can easily share resources between threads. Any global variables are shared for example; but good programmers avoid global variables because of the side-effects that can happen with them. Thankfully the shared data doesn't have to be a global variable. You can pass a list or dictionary to all threads so they sharing that single object.  Each thread has its own function stack. This means that local variables that are created in a thread are unique to that thread.

We will learn about other data elements that are used for sharing data between threads and processes later in the course.

### Thread Safe

> Thread safety is a computer programming concept applicable to multi-threaded code. Thread-safe code only manipulates shared data structures in a manner that ensures that all threads behave properly and fulfill their design specifications without unintended interaction. There are various strategies for making thread-safe data structures.

> A program may execute code in several threads simultaneously in a shared address space where each of those threads has access to virtually all of the memory of every other thread. Thread safety is a property that allows code to run in multithreaded environments by re-establishing some of the correspondences between the actual flow of control and the text of the program, by means of synchronization.

Modern concurrent and parallel programming languages will list which functions and data structures are "thread safe". This means that the function/data structure can be used in threads.  When programming in any language, you will need to review what is and isn't thread safe in that language. [Thread Safety in Python](https://python.plainenglish.io/thread-safety-in-python-7441f8627d46)

For example: in the language C++, the `rand()` function is not thread safe. If `rand()` is called in threads, the values returned by the `rand()` function will not be random.

Note that individual methods such as `append()` for list/set are thread safe in that if you call this method, you can be sure that the item was appended to the list/set. However, in most cases, you are doing more to a list/set/dict than just one method call. You can still have a race condition "between" the method statements.

### Race Conditions

Lets learn about race conditions by summarizing the [Race Condition Wikipedia](https://en.wikipedia.org/wiki/Race_condition) entry:

> A race condition arises in software when a computer program, to operate properly, depends on the sequence or timing of the program's processes or threads. Critical race conditions cause invalid execution and software bugs. Critical race conditions often happen when the processes or threads depend on some shared state. Operations upon shared states are done in critical sections that must be mutually exclusive. Failure to obey this rule can corrupt the shared state.

> A race condition can be difficult to reproduce and debug because the end result is nondeterministic and depends on the relative timing between interfering threads. Problems of this nature can therefore disappear when running in debug mode, adding extra logging, or attaching a debugger. Bugs that disappear like this during debugging attempts are often referred to as a "Heisenbug". It is therefore better to avoid race conditions by careful software design.

Assume that two threads each increment the value of a global integer variable by 1. Ideally, the following sequence of operations would take place: (Note that read and write below refers to reading the value from memory into the CPU and writing the value back to memory. This is also true when using CPU registers)

![](assets/race-1.png)

In the case shown above, the final value is 2, as expected. However, if the two threads run simultaneously without locking or synchronization, the outcome of the operation could be wrong. The alternative sequence of operations below demonstrates this scenario:

![](assets/race-2.png)

In this case, the final value is 1 instead of the correct result of 2. This occurs because here the increment operations are not mutually exclusive. Each thread can be removed from the `running` state and placed in the `waiting` state at any time. Mutually exclusive operations are those that cannot be interrupted while accessing some resource such as a memory location.

### Deadlock

Lets learn about deadlock by summarizing the [Deadlock Wikipedia](https://en.wikipedia.org/wiki/Deadlock) entry:

> In concurrent computing, a deadlock is a state in which each member of a group waits for another member, including itself, to take action, such as sending a message or more commonly releasing a lock. Deadlock is a common problem in multiprocessing systems, parallel computing, and distributed systems, where software and hardware locks are used to arbitrate shared resources and implement process synchronization.

> In an operating system, a deadlock occurs when a process or thread enters a waiting state because a requested system resource is held by another waiting process, which in turn is waiting for another resource held by another waiting process. If a process is unable to change its state indefinitely because the resources requested by it are being used by another waiting process, then the system is said to be in a deadlock.

For example:  Lets have two threads with two locks. The thread `thread1` will acquire lock `a` then `b`. Where, `thread2` will acquire lock `b` then `a`. Both threads will wait forever when causing a deadlock as each thread locks a lock that the other needs.

```python
a = Lock()
b = Lock()

def thread1(data):
    a.acquire()
    b.acquire()

    # do something

    b.release()
    a.release()

def thread2(data):
    b.acquire()
    a.acquire()

    # do something

    a.release()
    b.release()
```

### Synchronization Tools

In order to control access to shared resources between threads, you can use `locks` and `semaphores`.

**Locks**

We saw last lesson that a lock can be used to protect a critical section. For example you need to ensure that only 1 thread accesses a block of code as a time. Below is the coding example from last lesson. The lock in this case is global to the thread function, but it also could have been passed to the function as an argument.


```python
lock = threading.Lock()

def thread_func(filename, count):
    # acquire the lock before entering the critical section
    # If another thread has the lock, this thread will wait
    # until it's released.
    lock.acquire()
    
    # Do your stuff. Only 1 thread is running this code
    f = open(filename, 'w')
    f.write(count)
    f.close()

    # release the lock. If you fail to release the lock,
    # the next thread that tried to acquire the lock will
    # wait forever since the release will never happen.
    lock.release()
```

**Rules when using locks**

1. Don't over do it. The more locks you add to a program, the less parallel and concurrent it becomes. If you do need to use locks in your code, just use the minimum required. Remember that you don't lock threads, just shared data.
2. Try to keep the code in the critical section as small and fast as possible; treat acquiring and releasing locks like a game of hot potato. Since only one thread can enter a critical section at a time, all others are waiting. If you have a critical section that takes a long time to execute, then your program will be slow.
3. Try to limit any I/O statements such as accessing a file, writing to disk, print() statements, an so on. The reason for this, it that the thread making the I/O request will be placed on the `blocked` queue. **NEVER** put an `input()` statement in a critical section unless you have a really good reason (And I would like to hear it).

**Semaphore**

A semaphore is a synchronization primitive that allows multiple threads to access a shared resource in a controlled manner. It is essentially `a counter that is initialized to a certain value` (ie., an integer). When a thread wants to access the shared resource, it decrements the semaphore counter. If the counter is zero, the thread blocks until the counter is incremented by another thread. When a thread is finished with the shared resource, it increments the semaphore counter. `Note that a semaphore of value 1 is the same as a lock.`

For example, let's say you have a shared resource that can only be accessed by 3 threads at a time. You can use a semaphore to implement this by initializing the semaphore to 3. When a thread wants to access the shared resource, it calls the acquire() method on the semaphore. This method will decrement the semaphore counter. If the counter is zero, the method will block until the counter becomes greater than zero. When the thread is finished with the shared resource, it calls the release() method on the semaphore. This method will increment the semaphore counter.


We will cover semaphores in greater depth in a later lesson but for now here is a simple contrived example demonstrating how the code would work.  Please try the following code on your computer.  You will see that only three threads will get access to the function shared_resource() at a time.  When those 3 leave, 3 more threads will access the function.

```python
import threading
import time

def shared_resource(num):
    print(f'#{num}: I am the shared resource.')
    time.sleep(2)

def worker_thread(num, semaphore):
    # The with statement will decrease the semaphore by one.  If the semaphore is zero, then the thread
    # will wait until another thread is finished with the semaphore where it increments it by one
    with semaphore:
        shared_resource(num)

def main():
    threads = []

    # Allow 3 threads access to the critical section at a time
    semaphore = threading.Semaphore(3)

    for i in range(0, 10):
        thread = threading.Thread(target=worker_thread, args=(i, semaphore))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
```
