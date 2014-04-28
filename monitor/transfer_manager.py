__author__ = 'Alex Charters'
import requests
import time
import os
import json
from os.path import expanduser

base = "localhost:8000"
home_directory = str(expanduser("~") + "/")
file_out = home_directory + "OneDir/file_list.txt"


def file_strip(fullpath):
    head, tail = os.path.split(fullpath)
    return tail

def fold_strip(shortpath):
    head, tail = os.path.split(shortpath)
    return head

def directory_finder(fullpath):
    head, tail = os.path.split(fullpath)
    with_slash = head.split(home_directory)[1]
    without_slash = with_slash[1:]
    return without_slash

def upload_worker(string, cookbythebook):

    print "Creation subprocess started."

    filename = file_strip(string)
    #location = directory_finder(string)
    file_test = string.split("OneDir/monitor/")[1]
    folder = fold_strip(file_test)
    if filename.endswith("~"):
        print "No upload for ~ files."
    elif filename.startswith(".gout"):
        print "NO EXCEPTION TODAY!"
    else:
        directory = {'directory': folder}

        url = "http://"+ base +"/file_demo/upload_file/"
        response = requests.post(url,files={'file': open(file_test, 'rb')}, data=directory, cookies=cookbythebook)

        data = response.content[0:7000]
        print "Creation process finished for " + string + " ."
        new_dump = json.loads(data)
        with open(file_out, 'w') as file:
            json.dump(new_dump, file, indent=4)

def modified_worker(orig, dest_string, cookbythebook):

    print "Modification process started."
    if file_strip(orig).startswith(".gout"):
        print "File (" + dest_string + ") saved to the same file location."
        delete_worker(dest_string, cookbythebook)
        time.sleep(1)
        upload_worker(dest_string, cookbythebook)
    else:
        upload_worker(dest_string, cookbythebook)
        delete_worker(orig, cookbythebook)
        print "Modification process finished for " + orig + " to " + dest_string +"."



def delete_worker(string, cookbythebook):

    file = file_strip(string)
    #location = directory_finder(string)
    file_test = string.split("OneDir/monitor/")[1]
    folder = fold_strip(file_test)
    if not file.startswith(".gout"):
        directory = {'directory': folder, 'file': file}

        web = requests.post('http://'+ base +'/file_demo/delete_file/', data=directory, cookies=cookbythebook)
        data = web.content[0:7000]

        #replace old JSON file with new JSON response
        new_dump = json.loads(data)
        with open(file_out, 'w') as file:
            json.dump(new_dump, file, indent=4)
        print "Delete process finished for " + string + " ."
