__author__ = 'Alex'

import requests
from file_watcher import *
import json
from datetime import datetime
from os.path import expanduser

home = expanduser("~")
base = "ec2-54-86-59-86.compute-1.amazonaws.com:8000"
#base = "localhost:8000"
#url = "http://localhost:8000/file_demo/upload_file/"
#response = requests.post(url,files={'file': open('test.txt','rb')})


def check_datetime(secure_cookie):

    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
    rootdir = str(home) + '/OneDir/'
    upper_dir = str(home) + '/OneDir/monitor/'
    file_out = rootdir + 'file_list.txt'
    def read_json(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    def write_json(filename, data):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    def create_json(folder):
        write_json(folder+'file_list.txt', dict())


    web = requests.get('http://' + base + '/file_demo/json_request/',cookies=secure_cookie)
    server_json = json.loads(web.content)

    if not os.path.isfile(rootdir + 'file_list.txt'):
        create_json(rootdir)

    if os.path.isfile(rootdir + 'file_list.txt'):
        local_json = read_json(rootdir + 'file_list.txt')

    for item in server_json:
        time1 = datetime.strptime(server_json[item], DATETIME_FORMAT)
        if item in local_json:
            time2 = datetime.strptime(local_json[item], DATETIME_FORMAT)
            if time2 < time1:
                # fix parse


                file = item.split('/')[-1]
                direct = item.replace('/'+file, "")

                os.remove(home + "/OneDir/monitor/" + item)
                url = "http://" + base + "/file_demo/download_file/"
                directory = {'directory': direct, 'file': file}
                response = requests.post(url, data=directory, cookies=secure_cookie)
                local_json[item] = str(time1)
        elif item not in local_json:
            #fix parse

            file = item.split('/')[-1]
            #
            if item == file:
                direct = ""
            else:
                direct = item.replace('/'+file, "")
            url = "http://" + base + "/file_demo/download_file/"
            directory = {'directory': direct, 'file': file}
            response = requests.post(url, data=directory, cookies=secure_cookie)
            #FIGURE OUT HOW TO SAVE FILE RESPONSE
            print direct
            print home + "/OneDir/monitor/" + direct
            if not os.path.exists(home + "/OneDir/monitor/" + direct):
                os.makedirs(home + "/OneDir/monitor/" + direct)
            with open(item, 'wb') as f:
                for chunk in response.iter_content():
                    f.write(chunk)
            local_json[item] = str(time1)
    for item in local_json.keys():
        if item not in server_json:
            # fix parse
            file = item.split('/')[-1]
            os.remove(home + "/OneDir/monitor/" + item)
            del local_json[item]
    with open(file_out, 'w') as file:
            json.dump(local_json, file, indent=4)

def login():
    status_code = 0
    username = raw_input('Enter username:')
    password = raw_input('Enter password:')
    client = requests.session()
    client.get('http://' + base + '/file_demo/login/')
    csrf = client.cookies['csrftoken']
    #print csrf
    credentials = {'username': username, 'password': password}
    header = {'X-CSRFToken': csrf}
    web = client.post('http://' + base + '/file_demo/login/', data=credentials, headers=header)
    status_code = web.status_code
    secure_cookie = web.cookies
    while status_code !=200:
        print "incorrect combo!"
        username = raw_input('Enter username:')
        password = raw_input('Enter password:')
        client = requests.session()
        client.get('http://'+ base +'/file_demo/login/')
        csrf = client.cookies['csrftoken']
        #print csrf
        credentials = {'username': username, 'password': password}
        header = {'X-CSRFToken': csrf}
        web = client.post('http://'+ base +'/file_demo/login/', data=credentials, headers=header)
        status_code = web.status_code
        secure_cookie = web.cookies
    return secure_cookie


def register_user():
    status_code = 0
    print "Register for OneDir!"
    username = raw_input('Username:')
    credentials = {'username': username}
    web = requests.post('http://'+ base +'/file_demo/check_username/', data=credentials)
    status_code = web.status_code
    while status_code !=200:
        print "username is taken. Try again!"
        username = raw_input('Username:')
        credentials = {'username': username}
        web = requests.post('http://'+ base +'/file_demo/check_username/', data=credentials)
        status_code = web.status_code
    password = raw_input('Enter a Password (less than 20 characters):')
    while len(password) > 20:
        print "Password too long!"
        password = raw_input('Enter password again!')
    client = requests.session()
    client.get('http://'+ base +'/file_demo/login/')
    csrf = client.cookies['csrftoken']
    credentials = {'username': username, 'password': password}
    header = {'X-CSRFToken': csrf}
    web = client.post('http://'+ base +'/file_demo/register/', data=credentials, headers=header)
    secure_cookie = web.cookies
    print "registration successful!"
    return secure_cookie

def main():
    response = raw_input('Hello! Do you have an account? (y/n)')
    # while(response != 'y' or response != 'n'):
    #     response = input('Invalid response! Please type in y or n')
    if str(response).startswith('y'):
        secure_cookie = login()
        print "If you would like to change your password, please indicate so now."
        res = raw_input('Do you wish to change your password? (y or n):')
        if str(res).startswith('y'):
            change_password(secure_cookie)
        check_datetime(secure_cookie)
        print "starting onedir service..."
        print "=========================="
        print "WELCOME TO ONEDIR FILE SYNCHRONIZATION SERVICES"
        print "=========================="

        c = CombinedWatcher(secure_cookie)
        c.start()
    elif str(response).startswith('n'):
        secure_cookie = register_user()
        check_datetime(secure_cookie)
        print "staring onedir service..."
        print "========================"
        c = CombinedWatcher(secure_cookie)
        c.start()

    else:
        print "you suck"
        exit()

def change_password(secure_cookie):
    print "we have verified the shit out of you."
    new_password = raw_input('new password: ')
    while len(new_password) > 20:
        print "Password too long!"
        new_password = raw_input('Enter new password again!')
    client2 = requests.session()
    client2.get('http://'+ base + '/file_demo/change_password/')
    print client2.cookies
    csrf2 = client2.cookies['csrftoken']
    secure_cookie['csrftoken'] = None
    header2 = {'X-CSRFToken': csrf2}
    credential2 = {'password': new_password}
    web2 = client2.post('http://'+ base +'/file_demo/change_password/', data=credential2, headers=header2, cookies=secure_cookie)
    print web2.content[0:7000]
    print web2.status_code



if __name__ == "__main__":
    main()
