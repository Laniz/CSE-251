# Lesson 6 Prepare: Multiprocessing Module and Pipes

Section | Content
--- | ---
1   | [Overview](#overview)
2   | [Articles to Review](#articles-to-review)
3.1 | [Pipe](#pipe) :key:
3.2 | [Creating a Pipe](#creating-a-pipe)
3.3 | [Pipe Clarifications](#pipe-clarifications)
5   | [Sharing Data Between Processes](#sharing-data-between-processes) :key:

:key: = Vital concepts that we will continue to build on in coming lessons / key learning outcomes for this course.

### Overview

We will be covering two parts of the multiprocessing module: Pipe and Value. They are used to allow processes to share information between them.

### Articles to Review

- [Python Documentation](https://docs.python.org/3/library/multiprocessing.html#pipes-and-queues)
- [StackOverFlow: Pipe vs Queue](https://stackoverflow.com/questions/8463008/multiprocessing-pipe-vs-queue)
- [Python Shared Memory Between Processes](https://www.geeksforgeeks.org/multiprocessing-python-set-2/)
- [Pool, Process, Queue, and Pipe code examples](http://www.kasimte.com/multiprocessing-in-python-pool-process-queue-and-pipe)

### Pipe

Pipes are used to send messages (ie., data) between processes. The following is from the Python documentation on pipes. Note, that a pipe removes the need for a lock. The more locks in a program, the greater potential of it slowing down.

> When using multiple processes, one generally uses message passing for communication between processes and avoids having to use any synchronization primitives like locks.

### Creating a Pipe

When you create a pipe from the multiprocessing module, you receive both ends of the pipe. They are called the parent and child connections in most programming languages. For example, the parent will send information using their connection and the child will receive information using their connection. You can send information in both directions. Just be careful that you don't have both processes waiting for information at the same time or you will have created a deadlock.

```python
import multiprocessing 

# Unpack the pipe object (dictionary)
parent_connection, child_connection = multiprocessing.Pipe()
```

Just so you are aware the following code is equally valid but less common:

```python
import multiprocessing 

# Assign to a single variable instead of unpacking- like in the previous example.
pipes = multiprocessing.Pipe()

# Get the parent connection object using pipes['parent_conn'].
parent_conn = pipes['parent_conn']

# Get the child connection object using pipes['child_conn'].
child_conn = pipes['child_conn']
```

Here is an example of creating a pipe and passing the parent connection to the `sender` process and the child connection to the `receiver` process. Note that if a process tries to read from a pipe using `recv()` and there is nothing to read, then the process will wait. If nothing ever is sent on that pipe, you have a deadlock situation.

```python
import multiprocessing 

def sender(conn): 
    """ function to send messages to other end of pipe """
    conn.send('Hello')
    conn.send('World')
    conn.close() # Close this connection when done

def receiver(conn): 
    """ function to print the messages received from other end of pipe  """
    print(f'Received: {conn.recv()}')
    print(f'Received: {conn.recv()}')

if __name__ == "__main__": 

    # creating a pipe 
    parent_conn, child_conn = multiprocessing.Pipe() 

    # creating new processes 
    p1 = multiprocessing.Process(target=sender, args=(parent_conn,)) 
    p2 = multiprocessing.Process(target=receiver, args=(child_conn,)) 

    # running processes 
    p1.start() 
    p2.start() 

    # wait until processes finish 
    p1.join() 
    p2.join() 

```

Output:

```
Received: Hello
Received: World
```

### Pipe Clarifications

**Use close() Properly**

Do not forget to close both ends of your pipe! If you do not close both ends of a multiprocessing.Pipe, or never call close at all, the following things could happen:

- The pipe may not be garbage collected. This is because the pipe is still open in one or more processes, and the garbage collector cannot collect it until all of its references are gone. This can lead to memory leaks.
- Processes may block indefinitely when trying to read from the pipe. This is because the operating system may not know that the pipe has been closed, and the process may keep waiting for data that will never come.
- Processes may crash when trying to write to the pipe. This is because the operating system may close the pipe when the last process that had it open closes its connection. If another process tries to write to the pipe after this happens, it will cause an error.

**Pipe Communication**

As explained in the last section each `Pipe()` has two ends. You can imagine that these two ends operate like a traditional (old school) baby monitor. The listening device (sender, parent) picks up sound and transmits it to the receiving device (receiver, child).

![](./assets/baby-monitor.jpg)

This type of communication between processes is referred to as unidirectional (one-way) communication. Python does support bidirectional (both-way) communication between processes using **named pipes** but **we do not cover or use that in this class**.

**Named Pipes for the Curious**

If you are curious, named pipes are like a child's tin-can walkie-talkie. You can communicate (send data) and listen (receive data) from both ends of the tin-can walkie-talkie (Pipe).

![](./assets/tin-cans-string.jpg)

If you are only sending data in one direction however, a named pipe is overkill. Again, **we do not cover or use named pipes in this class**.

### Sharing Data Between Processes

Normally variables can't be shared between processes because each process has a complete copy of the program; their own GIL. However, there is a method for sharing data. We will need to use the `multiprocessing` module for this.

Here is an example from [the Python documentation website](https://docs.python.org/3/library/multiprocessing.html#sharing-state-between-processes)

[Data types for Value() function](https://docs.python.org/3/library/array.html#module-array)

```python
from multiprocessing import Process, Value, Array

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])
```

Output:

```
3.1415927
[0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
```

Here is a break down of the above example:

We need to import **Value** and/or **Array**. There are other methods of sharing data, but will wait later in the course to talk about them.

```python
from multiprocessing import Process, Value, Array
```

Next, we can use **Value** and/or **Array** to create the shared variables that will be used between processes. For both Value and Array, they take two arguments. 

- The first one is the data type. `d` indicates a double precision float and `i` indicates a signed integer.
- The second is the initial value for `Value()` or the list of values for `Array`.

```python
num = Value('d', 0.0)
arr = Array('i', range(10))
```

For other examples:

```python
count = Value('i', 0)   			   # create a shared integer count
counts = Array('i', [0, 0, 0, 0, 0])   # Create shared array of 5 values
```

Here we just pass them to the process using the `args` argument.

```python
p = Process(target=f, args=(num, arr))
```

Using these shared variables is a little different. For shared `Value()` variables, you need to use `.value` to use them. For the shared `Array()` variable, you access them normally using square brackets (`[]`).

```python
def f(n, a):
	n.value = 3.1415927
	for i in range(len(a)):
	    a[i] = -a[i]
```

When using shared variables, remember that if there are processes writing to and reading from them, then you need to stop a potential race condition by using a shared lock.