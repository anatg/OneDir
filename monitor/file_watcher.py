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
import client
base = "ec2-54-86-59-86.compute-1.amazonaws.com:8000"
#base = "192.168.164.129"




class OneDirHandler(FileSystemEventHandler):
    def __init__(self, cookie):
        self.cook = cookie

    def on_created(self, event):
        if event.is_directory is True:
            print "A directory was created: ( " + event.src_path + " )!"
        else:
            filepath = event.src_path

            if (filepath.endswith("client.py")) or (filepath.endswith("file_watcher.py")) or \
                    (filepath.endswith("transfer_manager.py")):
                print "Don't be touching my OneDir."
            else:
                p1 = multiprocessing.Process(target=upload_worker, args=(filepath, self.cook,))
                p1.start()


    def on_deleted(self, event):
        if event.is_directory is True:
            print "A folder was deleted: ( " + event.src_path + " )!"
        else:

            filepath = event.src_path
            if (filepath.endswith("client.py")) or (filepath.endswith("file_watcher.py")) or \
                    (filepath.endswith("transfer_manager.py")):
                print "Don't be touching my OneDir."
            else:
                p1 = multiprocessing.Process(target=delete_worker, args=(filepath, self.cook,))
                p1.start()

    def on_moved(self, event):
        if event.is_directory is True:
            print "Folder ( " + event.src_path + ") was renamed to ( " + event.dest_path + " )."
            # ALTER EVERYTHING CONTAINED IN SAID FOLDER
            #for filename in os.listdir():
             #   modified_worker()
        else:
            if (event.src_path.endswith("client.py")) or (event.dest_path.endswith("client.py")) or \
            (event.src_path.endswith("file_watcher.py")) or (event.dest_path.endswith("file_watcher.py")) or \
            (event.dest_path.endswith("transfer_manager.py")) or (event.dest_path.endswith("transfer_manager.py")):
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
        flag = True
        while flag:
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
                print "File synchronization temporarily stopped."
                print "Type 'restart' to turn back on file synchronization or " \
                      "'quit' to exit the OneDir."

                observer.stop()
            observer.join()
            reply = raw_input("restart or quit?")
            if reply == "restart":
                print "================"
                print "resynching onedir..."
                print "================"
                client.check_datetime(self.secured_cookie)
            elif reply == "quit":
                print "================"
                print "exiting onedir..."
                print "================"
                flag = False
            else:
                print "ouch, mistyping cost you, shutting down onedir"
                flag = False

