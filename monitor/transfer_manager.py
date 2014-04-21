__author__ = 'Alex Charters'
import requests
import time

def upload_worker(string, cookbythebook):
    #basic file created upload worker process
    print "Creation subprocess started."

    #parse from full filepath
    directory = {'directory': 'myfiles/supersecret'}
    url = "http://localhost:8000/file_demo/upload_file/"
    response = requests.post(url,files={'file': open(string, 'rb')}, data=directory, cookies=cookbythebook)
    print response.content[0:7000]
    print "Creation process finished for " + string + " ."

def modified_worker(string, cookbythebook):
    # file from server needs to be deleted
    # then upload the file to the server
    print "Modification process started."
    # INSERT FILE DELETE & UPLOAD COMBINATION
    #
    #
    #
    print "Modification process finished for " + string + " ."

def folder_worker(string):
    # insert code that detects when a folder is created
    # separate from created file
    # investigate how it is different in monitor
    print "File structure process started."
    #
    #
    #
    #
    print "File structure process finished for " + string + " ."

def delete_worker(string):
    # insert code for sending server request that deletes a file
    print "Delete process started."
    time.sleep(3)
    print "Delete process finished for " + string + " ."
