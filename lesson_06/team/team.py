"""
Course: CSE 251 
Lesson: L06 Team Activity
File:   team.py
Author: <Add name here>

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe
- Note, while getting your program to work, you can create a smaller text file instead of
  the ones given.  For example, create a text file with one line of text and get it to work
  with your program, then add another line of text and so on.
- After you can copy a text file word by word exactly, change the program (any way you want) to be
  faster (still using the processes).
"""

import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp 

# Include cse 251 common Python files
from cse251 import *

def sender(parent_conn, count): # Parent
    """ function to send messages to other end of pipe """
    '''
    open the file
    
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    '''
    with open('gettysburg.txt') as file:
        for line in file:
            text = line.strip().split()
            for word in text:
                parent_conn.send(word)
                parent_conn.send(' ')
            parent_conn.send('\r\n')
            count.value += 1

    parent_conn.send(None)
    parent_conn.close()

    


def receiver(child_conn): # Child
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
    while True:
        word = child_conn.recv()
        if word is None:
            break
        else:
            with open('gettysburg-copy.txt', 'a') as file:
                file.write(word)

    


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    # TODO create a pipe 
    parent_conn, child_conn = mp.Pipe()
    
    # TODO create variable to count items sent over the pipe
    count = Value('i', 0)

    # TODO create processes 

    log.start_timer()
    start_time = log.get_time()

    # TODO start processes 
    sender_process = Process(target=sender, args=(parent_conn, count))
    receiver_process = Process(target=receiver, args=(child_conn,))

    sender_process.start()
    receiver_process.start()
    
    # TODO wait for processes to finish
    sender_process.join()
    receiver_process.join()

    stop_time = log.get_time()

    # log.stop_timer(f'Total time to transfer content = {PUT YOUR VARIABLE HERE}: ')
    # log.write(f'items / second = {PUT YOUR VARIABLE HERE / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    # copy_file(log, 'bom.txt', 'bom-copy.txt')