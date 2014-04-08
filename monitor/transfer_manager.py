__author__ = 'Alex Charters'
import requests
import time

def upload_worker(string, cookcook):
    #basic file created upload worker process
    print "Creation subprocess started."
    #
    # client = requests.session()
    # client.get('http://localhost:8000/file_demo/login/')
    # csrf = client.cookies['csrftoken']
    # print csrf
    # credentials = {'username': 'test2', 'password':'password'}
    # header = {'X-CSRFToken': csrf}
    # web = client.post('http://localhost:8000/file_demo/login/', data=credentials, headers=header)
    # secure_cookie = web.cookies
    # print web.cookies
    # print web.content
    # web = requests.get('http://localhost:8000/file_demo/cookie_test/',cookies=secure_cookie)
    # print web.content
    directory = {'directory': 'myfiles/supersecret'}
    url = "http://localhost:8000/file_demo/upload_file/"
    response = requests.post(url,files={'file': open(string, 'rb')}, data=directory, cookies=cookcook)
    print response.content[0:7000]
    print "Creation process finished for " + string + " ."

def modified_worker(string):
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
