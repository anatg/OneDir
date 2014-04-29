__author__ = 'cls2be'

import json,os
from datetime import datetime

#Note This version of the json file protocol for OneDir will
# not have the entire file structure listed but rather
# each file individually listed with entire file path
#TODO: Organize json with folder structure

#SHould be called by view function that registers user
# Expects user's folder as input
# Creates user's json file
def create_json(folder):
    write_json(folder+'file_list.txt', dict())

#Should be called when a new file is added or edited by a user
# Expects full folder path
# including static file folder + directory + filename
def update_file(folder, new_file, full_path):
        json_file = folder+'file_list.txt'
        if os.path.isfile(full_path):
            os.remove(full_path)
        data = read_json(json_file)
        data[new_file] = str(datetime.utcnow())
        write_json(json_file, data)

#Should be called when a file is deleted by a user
# Expects full folder path
# Deletes file from json file if it exists
def delete_file(folder, new_file, full_path):
    json_file = folder+'file_list.txt'
    data = read_json(json_file)
    if new_file in data:
        del data[new_file]
    #if os.path.isfile(full_path):
        #os.remove(full_path)
    write_json(json_file, data)

#Function to read json file and return data
def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

#Function to write data to json file
def write_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def create_user_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def logger(logger_file, user, action, sync_file):
    with open(logger_file, 'a') as file:
        file.write(user + ' ' + action + ' ' + sync_file+'\n')