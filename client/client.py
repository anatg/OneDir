import requests

#Test file upload
#url = "http://localhost:8000/file_demo/upload_file/"
#response = requests.post(url,files={'file': open('test.txt','rb')})

#Test user login
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
# #web = requests.get('http://localhost:8000/file_demo/cookie_test/')
# print web.content

#Test registering a user
credentials = {'username': 'test3'}
web = requests.post('http://localhost:8000/file_demo/check_username/', data=credentials)
print web.status_code
if web.status_code == 200:
    client = requests.session()
    client.get('http://localhost:8000/file_demo/login/')
    csrf = client.cookies['csrftoken']
    credentials = {'username': 'test3', 'password':'password'}
    header = {'X-CSRFToken': csrf}
    web = client.post('http://localhost:8000/file_demo/register/', data=credentials, headers=header)
    secure_cookie = web.cookies
    print web.content
    print web.status_code
    web = requests.get('http://localhost:8000/file_demo/cookie_test/',cookies=secure_cookie)
    #web = requests.get('http://localhost:8000/file_demo/cookie_test/')
    print web.content


