__author__ = 'Anat'

import requests

#url = "http://localhost:8000/file_demo/upload_file/"
#response = requests.post(url,files={'file': open('test.txt','rb')})


def check_server(username, password):
    client = requests.session()
    client.get('http://localhost:8000/file_demo/login/')
    csrf = client.cookies['csrftoken']
    #print csrf
    credentials = {'username': username, 'password': password}
    header = {'X-CSRFToken': csrf}
    web = client.post('http://localhost:8000/file_demo/login/',data=credentials, headers=header)
    secure_cookie = web.cookies
    print web.content
    print web.cookies
    web = requests.get('http://localhost:8000/file_demo/cookie_test/')
    #web = requests.get('http://localhost:8000/file_demo/cookie_test/',cookies=secure_cookie)
    print web.content

def main():
    response = input('Hello! Do you have an account? (y/n)')
    if str(response).startswith('y'):
        username = input('Enter username:')
        password = input('Password:')
        #check = check_server(username, password)
        print check_server(username, password)
        if



if __name__ == "__main__":
    main()