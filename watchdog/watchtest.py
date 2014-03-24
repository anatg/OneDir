__author__ = 'Alex Charters'

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
import requests
url = "http://localhost:8000/file_demo/upload_file/"

class OneDirHandler(FileSystemEventHandler):

    def on_created(self, event):
        # Show loading
        response = requests.post(url,files={'file': open(event.src_path,'rb')})
        #Send finish loading signal

    def on_deleted(self, event):
        print "A file was deleted! ( " + event.src_path + " )!"

    def on_moved(self, event):
        # Renaming is the same as moving
        # Show loading
        print "Someone just took a trip to a new place..."
        # Send finish loading signal


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    # Custom overwrites of the functions
    #event_handler = OneDirHandler()

    # Records everything
    event_handler = LoggingEventHandler()

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()