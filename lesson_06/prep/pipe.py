import multiprocessing
import time

END_MESSAGE = None

def sender(conn): 
    """
    Function to send messages to other end of pipe:
    
    This will open a 'hallmark movie script' and parse it block of text by block of text. What it
    does is determine what the block is for, information or a person speaking for example, and then
    tags the data accordingly sending the 'package' (data) to the receiver to actually be printed.
    """
    with open('hallmark.txt') as file:
        for line in file:
            # Remove the newline from end of line and skip empty lines.
            txt = line.strip()
            if len(txt) < 1:
                continue
            
            # Determine who's line we are currently on so we can color them differently.
            print_type = 'INFO'
            colon_location = txt.find(':')
            if colon_location > -1 and colon_location < 10:
                print_type, _ = txt.split(':')

            conn.send([print_type, txt])
    
    conn.send(END_MESSAGE)
    conn.close() # Close this connection when done


def receiver(conn): 
    """ Function to print the messages received from other end of pipe  """
    while True:
        data = conn.recv()

        if data == END_MESSAGE:
            return
        
        print_type = data[0]
        movie_line = data[1]

        if print_type == 'ALEX':
            print(f'\033[34m{movie_line}\033[0m\n')
        elif print_type == 'BECKY':
            print(f'\033[35m{movie_line}\033[0m\n')
        else:
            print(f'\033[33m{movie_line}\033[0m\n')

        time.sleep(len(movie_line) * 0.07)


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
