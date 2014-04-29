__author__ = 'Alex Charters'
import requests
import time
import os
import json
from os.path import expanduser

#base = "localhost:8000"
base = "ec2-54-86-59-86.compute-1.amazonaws.com:8000"
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
    filename = file_strip(string)
    file_test = string.split("OneDir/monitor/")[1]
    folder = fold_strip(file_test)
    if filename.endswith("~"):
        print "No upload fired for temporary files."
    elif filename.startswith(".gout"):
        print "NO EXCEPTION TODAY!"
    else:
        print "Creation subprocess started."
        print "A file was created: ( " + string + " )!"
        directory = {'directory': folder}

        url = "http://"+ base +"/file_demo/upload_file/"
        response = requests.post(url,files={'file': open(file_test, 'rb')}, data=directory, cookies=cookbythebook)
        data = response.content

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



def delete_worker(filestring, cookbythebook):

    file = file_strip(filestring)
    file_test = filestring.split("OneDir/monitor/")[1]
    folder = fold_strip(file_test)
    if (not file.startswith(".gout")) and (not file.endswith("~")):
        print "Delete process started for ( " + filestring + " )."
        print "A file was deleted! ( " + filestring + " )!"
        directory = {'directory': folder, 'file': file}

        web = requests.post('http://'+ base +'/file_demo/delete_file/', data=directory, cookies=cookbythebook)
        data = web.content
        if web.status_code == 495:
            print "This file was not located on the OneDir server."
        else:
            new_dump = json.loads(data)
            with open(file_out, 'w') as file:
                json.dump(new_dump, file, indent=4)
        print "Delete process finished for " + filestring + " ."
