"""
Author: Brother Keers

This script demonstrates the concept of using a multithreading Pool to process a
list of books in the scriptures. In this demo we print the name on a delay so
you can see how different processes are handling the processing. Assuming you did
not create a pool bigger than your computers CPU core count, each process should
be on its own CPU core and is truly running in parallel.

- Why is it important to create a pool less than or equal to your CPU core count?
- What are some limitations to using a pool?
"""

import multiprocessing as mp
import os
import time

def print_book_name(book):
    """ Print the name of a book of scriptures along with the process ID that ran this function. """
    time.sleep(0.5)
    print(f'{book:.<20} {os.getpid()}')


def main():

    books_of_scripture = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', '1 Nephi', '2 Nephi', 'Jacob', 'Enos', 'Jarom', 'Omni', 'Words of Mormon', 'Mosiah', 'Alma', 'Helaman', '3 Nephi', '4 Nephi', 'Mormon', 'Ether', 'Moroni']

    print(f'Book of Scripture    Process ID\n{"-" * 31}')

    # Create a pool of 2 processes
    with mp.Pool(2) as p:
        """
        Map these 2 processes to the function print_book_name(). Python will create 2 processes that
        run in parallel, each calling print_book_name() and alternating between items in the list.

        You can not send in more than one argument to the mapped function and a list is expected.
        """
        p.map(print_book_name, books_of_scripture)


# Protect the call to main
if __name__ == '__main__':
    main()