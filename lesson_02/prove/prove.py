"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: Shepherd Ncube

4 meets the requirements. The code runs under 10 seconds, and no global variables are used.

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py" and leave it running.
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}

Outline of API calls to server

1) Use TOP_API_URL to get the dictionary above
2) Add "6" to the end of the films endpoint to get film 6 details
3) Use as many threads possible to get the names of film 6 data (people, starships, ...)
"""

from datetime import datetime
import requests
import threading
from cse251 import *

TOP_API_URL = 'http://127.0.0.1:8790'
call_count = 0  # Global variable for tracking API calls

class APIthread(threading.Thread):
    def __init__(self, url, results, index, call_count_lock):
        super().__init__()
        self.url = url
        self.results = results
        self.index = index
        self.call_count_lock = call_count_lock

    def run(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            self.results[self.index] = data.get('name', 'Unknown')
        else:
            self.results[self.index] = 'Error'
        with self.call_count_lock:
            global call_count
            call_count += 1

def fetch_data(urls, call_count_lock):
    results = [None] * len(urls)
    threads = [APIthread(url, results, i, call_count_lock) for i, url in enumerate(urls)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return sorted(results)

def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # Fetch Top API URLs
    response = requests.get(TOP_API_URL)
    if response.status_code != 200:
        print("Failed to connect to the server.")
        return
    api_urls = response.json()

    # print(f"\n\n this is the api url {api_urls} \n\n")

    # Fetch Film 6 Details
    film_6_url = api_urls['films'] + '6'

    print(f"\n\n this is the api for film 6 {film_6_url} \n\n")

    response = requests.get(film_6_url)
    if response.status_code != 200:
        print("Failed to retrieve film 6 data.")
        return
    film_6_data = response.json()

    # Fetch related data using threads
    call_count_lock = threading.Lock()
    categories = ['characters', 'planets', 'starships', 'vehicles', 'species']

    for category in categories:
        urls = film_6_data.get(category, [])
        names = fetch_data(urls, call_count_lock)
        log.write(f'{category.capitalize()}: {len(names)}')
        if names:
            log.write(f'  {", ".join(names)}')  # Combine all names in a single line

    # Stop timer and log the total time
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')

if __name__ == "__main__":
    main()
