__author__ = 'Alex Charters'

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from transfer_manager import upload_worker, delete_worker, modified_worker
import multiprocessing
import os

base = "192.168.164.129"




class OneDirHandler(FileSystemEventHandler):
    def __init__(self, cookie):
        self.cook = cookie

    def on_created(self, event):
        if event.is_directory is True:
            print "A directory was created: ( " + event.src_path + " )!"
        else:
            filepath = event.src_path

            if (filepath.endswith("client3.py")) or (filepath.endswith("file_watcher.py")) or \
                    (filepath.endswith("transfer_manager.py")):
                print "Don't be touching my OneDir."
            else:

                print "A file was created: ( " + event.src_path + " )!"

                p1 = multiprocessing.Process(target=upload_worker, args=(filepath, self.cook,))
                p1.start()


    def on_deleted(self, event):
        if event.is_directory is True:
            print "A folder was deleted: ( " + event.src_path + " )!"
        else:

            filepath = event.src_path
            if (filepath.endswith("client3.py")) or (filepath.endswith("file_watcher.py")) or \
                    (filepath.endswith("transfer_manager.py")):
                print "Don't be touching my OneDir."
            else:
                print "A file was deleted! ( " + event.src_path + " )!"
                p1 = multiprocessing.Process(target=delete_worker, args=(filepath, self.cook,))
                p1.start()

    def on_moved(self, event):
        if event.is_directory is True:
            print "Folder ( " + event.src_path + ") was renamed to ( " + event.dest_path + " )."
            # ALTER EVERYTHING CONTAINED IN SAID FOLDER
            #for filename in os.listdir():
             #   modified_worker()
        else:
            if (event.src_path.endswith("client3.py")) or (event.dest_path.endswith("client3.py")) or \
            (event.src_path.endswith("file_watcher.py")) or (event.dest_path.endswith("file_watcher.py")) or \
            (event.dest_path.endswith("transfer_manager.py"))(event.dest_path.endswith("transfer_manager.py")):
                print "Don't be touching my OneDir."
            else:

                n_filepath = event.dest_path
                o_filepath = event.src_path


                print "The file " + event.src_path + " was modified."
                p1 = multiprocessing.Process(target=modified_worker, args=(o_filepath,n_filepath, self.cook,))

                p1.start()
                p1.join()



class CombinedWatcher:
    def __init__(self, cookie):
        self.secured_cookie = cookie
    def start(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        path = sys.argv[1] if len(sys.argv) > 1 else '.'

        # Custom overwrites of the functions
        event_handler = OneDirHandler(self.secured_cookie)

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

