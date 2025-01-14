# Lesson 4 Team Teaching: Using Queues and Semaphores

### Overview

Today's team activity will be using queue(s) and thread's with semaphore(s). 

### Assignment

The file `urls.txt` contains a list of URLs for the program `server.py`. You will need to start the `server.py` program in a separate terminal for this team activity to work; this is the same server used in Lesson 2. You will be creating a thread that will read this data file line by line and placing the URLs into a queue. The other thread(s) will take URLs from the queue and request information using that URL. Use the `request` module for internet requests.

### Instructions

- **NO global variables!**
- Do not use thread/process pools for this program.
- Use only the provided packages that are imported.
- Review all of the given code so you understand it before adding your code.
- I would suggest setting RETRIEVE_THREADS to 1 and get that to work first before increasing it.

### Requirements

1. In a terminal (mac) or command window (windows), run the server with the command `python server.py` for Windows, `python3 server.py` for Mac; or possibly with the alias command `py` depending on your operating system. You can check the documentation for the Lesson 2 Prove assignment on how to run the server; usually `python server.py` or `python3 server.py` but sometimes `py server.py` instead.
2. Start with `RETRIEVE_THREADS = 1` while implementing the threads. Implement your program in steps, building on code that works.
3. You final goal is to set `RETRIEVE_THREADS = 4` where you will create 4 `retrieve_thread()` threads.
4. Once you have the program working with multiple threads, run the program using different `RETRIEVE_THREADS` values. Does your program complete faster with more threads?  Is there a point where adding more threads to this program doesn't improve completion time?

### Sample Solution

We will go over a solution in class this week.

### Submission

When complete, please report your progress in the associated Canvas quiz.
