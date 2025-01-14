"""
Course: CSE 251
Lesson: L02 Team Activity
File:   team-solution.py
Author: Brother Comeau

Purpose: Make threaded API calls with the Playing Card API http://deckofcardsapi.com
"""

from datetime import datetime, timedelta
import threading
import requests
import json

# # Include cse 251 common Python files
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


class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        req = Request_Thread(rf'https://deckofcardsapi.com/api/deck/{self.id}/shuffle/')
        req.start()
        req.join()


    def draw_card(self):
        req = Request_Thread(rf'https://deckofcardsapi.com/api/deck/{self.id}/draw/')
        req.start()
        req.join()
        if req.status_code == 200 and req.response != {}:
            self.remaining = req.response['remaining']
            return req.response['cards'][0]['code']
        else:
            return ''

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # DONE: Run the program team_get_deck_id.py ONCE and insert the deck ID here.
    deck_id = 'CODE'

    deck = Deck(deck_id)

    for i in range(55):
        card = deck.draw_endless()
        print(f'Card {i + 1}: {card}', flush=True)

    print()