"""
Course: CSE 251
Lesson: L02 Team Activity
File:   team_get_deck_id.py
Author: Brother Comeau

Purpose: Playing Card deck ID

Instructions:

- Run this once to get a ID to be used in the team.py program.
"""

import requests
import json
import threading
from datetime import datetime, timedelta

# Include cse 251 common Python files
from cse251 import *


class Request_Thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        # threading.Thread.__init__(self)
        super().__init__()
        self.url = url
        self.response = {}
        self.status_code = 0

    def run(self):
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        self.status_code = response.status_code
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)

if __name__ == '__main__':

    response = requests.get(r'https://deckofcardsapi.com/api/deck/new/')

    # Check the status code to see if the request succeeded.
    if response.status_code == 200:
        data = response.json()

        # Function is from the cse251 common code 
        print_dict(data)

        if 'success' in data:
            if data['success'] == True:
                print(data['deck_id'])
            else:
                print('Error in requesting ID')
        else:
            print('Error in requesting ID')
    else:
        print('Error in requesting ID')
