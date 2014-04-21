__author__ = 'Alex Charters'

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from transfer_manager import upload_worker, delete_worker, modified_worker
import multiprocessing

master_queue = multiprocessing.JoinableQueue()

class OneDirHandler(FileSystemEventHandler):

    def on_created(self, event):
        filepath = event.src_path
        #response = requests.post(url,files={'file': open(event.src_path,'rb')})
        print "A file was created: ( " + event.src_path + " )!"
        p1 = multiprocessing.Process(target=upload_worker, args=(filepath, CombinedWatcher.secured_cookie,))
        #master_queue.put_nowait(p1)
        p1.start()
        #Send finish loading signal

    def on_deleted(self, event):
        filepath = event.src_path
        print "A file was deleted! ( " + event.src_path + " )!"
        p1 = multiprocessing.Process(target=delete_worker, args=(filepath, CombinedWatcher.secured_cookie,))
        #master_queue.put_nowait(p1)
        p1.start()

    def on_moved(self, event):
        filepath = event.src_path
        # Renaming is the same as moving
        # Show loading
        print "The file " + event.src_path + " was modified."
        p1 = multiprocessing.Process(target=modified_worker, args=(filepath, CombinedWatcher.secured_cookie,))
        # master_queue.put_nowait(p1)
        p1.start()

class CombinedWatcher:
    secured_cookie = None
    def __init__(self, cookie):
        secured_cookie = cookie
    def start(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        path = sys.argv[1] if len(sys.argv) > 1 else '.'

        # Custom overwrites of the functions
        event_handler = OneDirHandler()

        # Records everything
        #event_handler = LoggingEventHandler()

        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

