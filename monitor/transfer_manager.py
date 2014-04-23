__author__ = 'Alex Charters'
import requests
import time
import os

def file_strip(fullpath):
    temp = ""
    return fullpath.split(temp)[1]

def upload_worker(string, cookbythebook):
    #basic file created upload worker process
    print "Creation subprocess started."
    #NEED TO PARSE FROM FULL FILEPATH
    directory = {'directory': ''}
    url = "http://localhost:8000/file_demo/upload_file/"
    response = requests.post(url,files={'file': open('test.txt', 'rb')}, data=directory, cookies=cookbythebook)
    print response.content[0:7000]
    print "Creation process finished for " + string + " ."

def modified_worker(string, cookbythebook):
    # file from server needs to be deleted
    # then upload the file to the server
    print "Modification process started."
    # INSERT FILE DELETE & UPLOAD COMBINATION
    # File Delete
    #directory = {'directory': 'myfiles/supersecret'}
    #web = requests.post('http://localhost:8000/file_demo/delete_file/', data=directory, cookies=cookbythebook)
    #print web.content[0:7000]

    #File Upload
    #url = "http://localhost:8000/file_demo/upload_file/"
    #response = requests.post(url,files={'file': open(string, 'rb')}, data=directory, cookies=cookbythebook)
    #print response.content[0:7000]
    # File Upload

    print "Modification process finished for " + string + " ."

def folder_worker(string, cookbythebook):
    # insert code that detects when a folder is created
    # separate from created file
    # investigate how it is different in monitor
    print "File structure process started."
    #
    #
    #
    #
    print "File structure process finished for " + string + " ."

def delete_worker(string, cookbythebook):
    # insert code for sending server request that deletes a file
    # URL PARSE FROM FILEPATH TO FIT DIRECTORY

    #directory = {'directory': 'myfiles/supersecret', 'file': 'test1.txt'}
    #web = requests.post('http://localhost:8000/file_demo/delete_file/', data=directory, cookies=cookbythebook)
    #print web.content[0:7000]
    print "Delete process finished for " + string + " ."
