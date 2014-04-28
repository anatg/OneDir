__author__ = 'Anat'
import requests

from django.conf import settings


#url = "http://localhost:8000/file_demo/upload_file/"
#response = requests.post(url,files={'file': open('test.txt','rb')})

def check_datetime(secure_cookie):
    import os
    import json
    from datetime import datetime
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    rootdir = '/home/OneDir/monitor/'

    def read_json(filename):
        with open(filename, 'r') as file:
            return json.loads(file)
    def write_json(filename, data):
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    def create_json(folder):
        write_json(folder+'file_list.txt', dict())


    web = requests.get('http://localhost:8000/file_demo/json_request/',cookies=secure_cookie)
    server_json = json.loads(web.content)
    if not os.path.isfile(rootdir + 'file_list.txt'):
        create_json(rootdir)
    if os.path.isfile(rootdir + 'file_list.txt'):
        local_json = read_json('file_list.txt')
    for item in server_json:
        time1 = datetime.strptime(server_json[item], DATETIME_FORMAT)
        if item in local_json:
            time2 = datetime.strptime(local_json[item], DATETIME_FORMAT)
            if time2 < time1:
                cwd = str(os.getcwd()).split('monitor/', 1)[1]
                file = cwd.split('/')[-1]
                cwd = cwd.replace('/'+file, "")
                os.remove(file)
                url = "http://localhost:8000/file_demo/download_file/"
                directory = {'directory': cwd, 'file': file}
                response = requests.post(url, data=directory, cookies=secure_cookie)
                local_json[item] = str(time1)
        elif item not in local_json:
            file = str(item).split('monitor/', 1)[1].split('/')[-1]
            diction  = str(item).split('monitor/', 1)[-1].replace('/'+file, "")
            url = "http://localhost:8000/file_demo/download_file/"
            directory = {'directory': diction, 'file': file}
            response = requests.post(url, data=directory, cookies=secure_cookie)
            local_json[item] = str(time1)
    for item in local_json and (item not in server_json):
        cwd = str(os.getcwd()).split('monitor/', 1)[1]
        file = cwd.split('/')[-1]
        cwd = cwd.replace('/'+file, "")
        os.remove(file)

def login():
    status_code = 0

    username = raw_input('Enter username:')
    password = raw_input('Enter password:')
    client = requests.session()
    client.get('http://localhost:8000/file_demo/login/')
    csrf = client.cookies['csrftoken']
    #print csrf
    credentials = {'username': username, 'password': password}
    header = {'X-CSRFToken': csrf}
    web = client.post('http://localhost:8000/file_demo/login/', data=credentials, headers=header)
    status_code = web.status_code
    secure_cookie = web.cookies
    while status_code !=200:
        print "incorrect combo!"
        username = raw_input('Enter username:')
        password = raw_input('Enter password:')
        client = requests.session()
        client.get('http://localhost:8000/file_demo/login/')
        csrf = client.cookies['csrftoken']
        #print csrf
        credentials = {'username': username, 'password': password}
        header = {'X-CSRFToken': csrf}
        web = client.post('http://localhost:8000/file_demo/login/', data=credentials, headers=header)
        status_code = web.status_code
        secure_cookie = web.cookies
    return secure_cookie




def register_user():
    status_code = 0
    print "Register for OneDir!"
    username = raw_input('Username:')
    credentials = {'username': username}
    web = requests.post('http://localhost:8000/file_demo/check_username/', data=credentials)
    status_code = web.status_code
    while status_code !=200:
        print "username is taken. Try again!"
        username = raw_input('Username:')
        credentials = {'username': username}
        web = requests.post('http://localhost:8000/file_demo/check_username/', data=credentials)
        status_code = web.status_code
    password = raw_input('Enter a Password (less than 20 characters):')
    while len(password) > 20:
        print "Password too long!"
        password = raw_input('Enter password again!')
    client = requests.session()
    client.get('http://localhost:8000/file_demo/login/')
    csrf = client.cookies['csrftoken']
    credentials = {'username': username, 'password': password}
    header = {'X-CSRFToken': csrf}
    web = client.post('http://localhost:8000/file_demo/register/', data=credentials, headers=header)
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
        print "starting onedir service..."
    elif str(response).startswith('n'):
        secure_cookie = register_user()
        print "staring ondir service..."
        check_datetime(secure_cookie)
    else:
        print "uh oh"
        exit()

def change_password(secure_cookie):
    print "we have verified you"
    new_password = raw_input('new password: ')
    while len(new_password) > 20:
        print "Password too long!"
        new_password = raw_input('Enter new password again!')
    client2 = requests.session()
    client2.get('http://localhost:8000/file_demo/change_password/')
    print client2.cookies
    csrf2 = client2.cookies['csrftoken']
    secure_cookie['csrftoken'] = None
    header2 = {'X-CSRFToken': csrf2}
    credential2 = {'password': new_password}
    web2 = client2.post('http://localhost:8000/file_demo/change_password/', data=credential2, headers=header2, cookies=secure_cookie)
    print web2.content[0:7000]
    print web2.status_code



if __name__ == "__main__":
    main()