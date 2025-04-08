"""
Course: CSE 251, week 14
File: functions.py
Author: <your name>

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
family_id = 6128784944
request = Request_thread(f'{TOP_API_URL}/family/{family_id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
person_id = 2373686152
request = Request_thread(f'{TOP_API_URL}/person/{person_id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

<Add your comments here>


Describe how to speed up part 2

<Add your comments here>


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *
import queue
from threading import Lock, Semaphore

# -----------------------------------------------------------------------------
from concurrent.futures import ThreadPoolExecutor, as_completed

def depth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement Depth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging
    if tree.does_family_exist(family_id):
        return
    family_request = Request_thread(f"{TOP_API_URL}/family/{family_id}")
    family_request.start()
    family_request.join()

    family_data = family_request.get_response()
    family = Family(family_data)
    tree.add_family(family)

    person_threads = []
    recursive_threads = []
    for person_id in [family.get_husband(), family.get_wife()] + family.get_children():
        if person_id and not tree.does_person_exist(person_id):
            person_thread = Request_thread(f"{TOP_API_URL}/person/{person_id}")
            person_threads.append(person_thread)
            # person_thread.start()
    for thread in person_threads:
        thread.start()
    for thread in person_threads:
        thread.join()
        person_data = thread.get_response()
        if person_data:
            person = Person(person_data)
            tree.add_person(person)

            parent_family_id = person.get_parentid()
            if parent_family_id and not tree.does_family_exist(parent_family_id):
                recursive_thread = threading.Thread(
                    target=depth_fs_pedigree, args=(parent_family_id, tree)
                )
                recursive_threads.append(recursive_thread)
                recursive_thread.start()

    for thread in recursive_threads:
        thread.join()



    # -----------------------------------------------------------------------------    
def breadth_fs_pedigree(family_id, tree):
    visited = {family_id: True}
    queue = [family_id]
    lock = Lock()

    while queue:
        next_queue = []
        threads = []

        def process_family(fid):
            req = Request_thread(f'{TOP_API_URL}/family/{fid}')
            req.start()
            req.join()
            family_data = req.get_response()
            if not family_data:
                return

            family = Family(family_data)
            with lock:
                tree.add_family(family)

            person_threads = []
            person_ids = [family.get_husband(), family.get_wife()] + family.get_children()
            for pid in person_ids:
                if pid is None:
                    continue
                with lock:
                    if tree.does_person_exist(pid):
                        continue
                t = Request_thread(f'{TOP_API_URL}/person/{pid}')
                t.start()
                person_threads.append((pid, t))

            for pid, t in person_threads:
                t.join()
                pdata = t.get_response()
                if pdata:
                    with lock:
                        tree.add_person(Person(pdata))

            with lock:
                for pid in [family.get_husband(), family.get_wife()]:
                    person = tree.get_person(pid)
                    if person:
                        parent_id = person.get_parentid()
                        if parent_id and parent_id not in visited:
                            visited[parent_id] = True
                            next_queue.append(parent_id)

        for fid in queue:
            t = threading.Thread(target=process_family, args=(fid,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        queue = next_queue


    # -----------------------------------------------------------------------------    
def breadth_fs_pedigree_limit5(family_id, tree, max_threads=5):
    visited = {family_id: True}
    queue = [family_id]
    lock = Lock()
    semaphore = Semaphore(max_threads)

    while queue:
        next_queue = []
        threads = []

        def process_family(fid):
            with semaphore:
                req = Request_thread(f'{TOP_API_URL}/family/{fid}')
                req.start()
                req.join()
                family_data = req.get_response()
                if not family_data:
                    return

                family = Family(family_data)
                with lock:
                    tree.add_family(family)

                person_threads = []
                person_ids = [family.get_husband(), family.get_wife()] + family.get_children()
                for pid in person_ids:
                    if pid is None:
                        continue
                    with lock:
                        if tree.does_person_exist(pid):
                            continue
                    t = Request_thread(f'{TOP_API_URL}/person/{pid}')
                    t.start()
                    person_threads.append((pid, t))

                for pid, t in person_threads:
                    t.join()
                    pdata = t.get_response()
                    if pdata:
                        with lock:
                            tree.add_person(Person(pdata))

                with lock:
                    for pid in [family.get_husband(), family.get_wife()]:
                        person = tree.get_person(pid)
                        if person:
                            parent_id = person.get_parentid()
                            if parent_id and parent_id not in visited:
                                visited[parent_id] = True
                                next_queue.append(parent_id)

        for fid in queue:
            t = threading.Thread(target=process_family, args=(fid,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        queue = next_queue
