from flask import Flask
import json
import os
import logging

"""
Demo of server using Flask.  Can be used by either:
a) typing URLs into a webbrowser's address box, or
b) by a client sending it HTTP requests. A sample client is provided, requests_client1.py.

3rd party libraries to be installed:
a) Flask

Note: PyCharm allows you to create a new project for Flask.  This was created using that. Try it.

This program also shows how to use logging in Python. Logging libraries are used in real software
to provide informational messages.  Especially for servers.  See this link for more info:
http://docs.python.org/2/howto/logging.html#logging-basic-tutorial

Important: this command:   http://127.0.0.1:5000/get-file-data/somedata.txt
requires that there be a subdirectory called 'filestore' in the folder given by the
variable WORKING_DIR defined below.  This command will look for a file called
'somedata.txt' in that folder. So to see this work, you must adjust WORKING_DIR,
create the subdirectory, and put a file or files in there.

"""

app = Flask(__name__)

WORKING_DIR = '/Users/Anat/Projects/od/'


# Invoked when you access: http://127.0.0.1:5000
@app.route('/')
def hello_world():
    logging.debug("entering hello_world")
    return 'Hello World!'

# Invoked when you access: http://127.0.0.1:5000/hi
@app.route('/hi')
def hi_world():
    logging.debug("entering hi_world")
    return 'Hi World!'


# Invoked when you access: http://127.0.0.1:5000/get-json
@app.route('/get-json')
def get_json1():
    logging.debug("entering get_json")
    data = [1, 2, "three"]
    ret = json.dumps(data)
    return ret


# Invoked when you access: http://127.0.0.1:5000/get-file-data/somedata.txt
@app.route('/get-file-data/<filename>')
def get_file_data(filename):
    logging.debug("entering get_file_data")
    full_filename = os.path.join(WORKING_DIR, 'filestore', filename)
    if not os.path.exists(full_filename):
        logging.warn("file does not exist on server: " + full_filename)
        ret_value = { "result" : -1, "msg" : "file does not exist"}
    else:
        with open(full_filename, "rb") as in_file:
            snippet = in_file.read(32)
        file_size = os.path.getsize(full_filename)
        ret_value = { "result" : 0, "size" : file_size, "value" : snippet}
    return json.dumps(ret_value)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(filename='example.log',level=logging.DEBUG)
    logging.info("Starting server")
    app.run()
