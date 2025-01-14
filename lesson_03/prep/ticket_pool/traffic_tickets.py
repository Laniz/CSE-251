"""
Author: Brother Keers

This script demonstrates how a pool could be used to solve a real life problem:

The State of Western Australia, Australia, has hundreds of speeding cameras that automatically
capture people speeding. After a verification process, all the tickets are processed in batches and
mailed out to violators on a weekly basis. In this example a batch of tickets is loaded from a json
file (`tickets.json`), which is simulating a database in this demo, and then processed. To process
a ticket we first must determine the amount of the fine -- see the process_ticket() function -- and
then we must mail it -- see the mail_infraction() function -- to the violator.
"""

import json
import timeit
import time
import multiprocessing as mp

# Constants we need for this demo.
ALL_CPU_CORES  = mp.cpu_count()
HALF_CPU_CORES = mp.cpu_count() // 2
PROCESSORS     = [HALF_CPU_CORES, ALL_CPU_CORES]


def mail_infraction(ticket_number, name, license, fine):
    """
    Called by `process_ticket` to mail out the fine. In reality this function would most likely call
    an API to save this data or interface with a printing system of some kind to actually print the
    ticket (fine).

    Parameters:
        ticket_number (str): The unique ticket number.
        name (str): The name of the violator.
        license (str): The license number of the violator.
        fine (float): The amount owed.
    """

    # Show the demo processing tickets by printing out the current ticket number.
    print(f'{ticket_number}', end=' ', flush=True)

    # Pretend to do something since in real life we would actually do something here.
    time.sleep(0.001)


def process_ticket(ticket):
    """
    The target function for the Pool. Accepts a ticket object (dictionary), determines the correct
    fine amount, and then calls `mail_infraction` to complete processing this ticket.

    ticket = {
        "ticket": [unique ticket number],
        "name": [violators name],
        "license": [violators drivers license number],
        "zone": [posted speed limit],
        "speed": [speed violator was clocked driving]
    }

    Parameter:
        ticket (dict): The ticket object.
    """

    # Setup needed variables.
    fine    = 0
    over_by = ticket['speed'] - ticket['zone']

    # Determine the fine based on how many kph over the speed limit they were driving.
    if over_by <= 5:
        fine = 65.50
    elif over_by <= 10:
        fine = 110.50
    elif over_by <= 15:
        fine = 155.75
    else:
        fine = 325.00

    # Complete processing this ticket by mailing it out (or printing it) now.
    mail_infraction(ticket['ticket'], ticket['name'], ticket['license'], fine)


def main():
    """
    Since this is a demo we get the batch of tickets from a json file. In a real production
    application we probably would have grabbed this from a database or API.
    """
    tickets = []
    try:
        with open('tickets.json', 'r') as file:
            tickets = json.load(file)
    except:
        print('WARNING:\nCould not load required files! Do not use the `play` button in VS Code to run this file. Manually run this\nfile from the terminal/console and make sure your not missing `ticket_info.json` and `ticket_numbers.json`.')
        return

    # To make the demo take longer to process duplicate the batch of tickets.
    tickets += tickets

    """
    Keep track of how long it takes to process a batch of tickets with half your available processors
    and then all your available processors. Tracking time this way IS NORMALLY NOT NEEDED but we do
    it here so the demo output looks nicer.
    """
    times = []

    # Keep track of how long this whole operation takes.
    all_process_time = timeit.default_timer()

    # Demo processing a batch of tickets with half your available processors and then all of them.
    for processors in PROCESSORS: # Should only loop 2 times in this demo.
        # Track how long it takes to process a batch of tickets with `processor` amount of processes.
        start_time = timeit.default_timer()
        with mp.Pool(processors) as pool:
            pool.map(process_ticket, tickets)
        times.append(timeit.default_timer() - start_time)
    
    # Show all the times we have been tracking
    print()
    for i, runtime in enumerate(times):
        print(f'Time for {len(tickets)} tickets using {PROCESSORS[i]} processes: {runtime}')
    print(f'Total time for ALL processing: {timeit.default_timer() - all_process_time}')


# Protect the call to main
if __name__ == '__main__':
    main()