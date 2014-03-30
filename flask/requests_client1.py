__author__ = 'tbh3f'

import requests
import json

HOST = 'http://127.0.0.1:5000/'


def process_file(filename):
    print "\n* Getting info about file '", filename, "' on server:"
    url = HOST + "get-file-data/" + filename
    r = requests.get(url)

    response = r.json()
    print "JSON response from server: ", response
    if response["result"] == 0:
        print "File size: ", response["size"]
        print "First 32 bytes of file: ", response["value"]
    else:
        print "Error: response code=", response["result"], ", reason=", response["msg"]

def main():
    # let's try some things out
    r = requests.get('http://127.0.0.1:5000/get-json')
    print r.text
    print r.json()

    list = r.json()
    for i in list:
        print i

    # We could do something like the next line, but let's write a function to do this
    # r = requests.get('http://127.0.0.1:5000/get-file-data/somedata.txt')

    process_file("README.md")
    process_file("badfile")

    print "\nClient ending."


if __name__ == "__main__":
    main()