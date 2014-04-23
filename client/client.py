import requests

#Test original simple file upload
#url = "http://localhost:8000/file_demo/upload_file/"
#response = requests.post(url,files={'file': open('test.txt','rb')})

#Test user login
# client = requests.session()
# client.get('http://localhost:8000/file_demo/login/')
# csrf = client.cookies['csrftoken']
# #print csrf
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
# credentials = {'username': 'test4'}
# web = requests.post('http://localhost:8000/file_demo/check_username/', data=credentials)
# print web.status_code
# if web.status_code == 200:
#     client = requests.session()
#     client.get('http://localhost:8000/file_demo/register/')
#     csrf = client.cookies['csrftoken']
#     credentials = {'username': 'test4', 'password':'password'}
#     header = {'X-CSRFToken': csrf}
#     web = client.post('http://localhost:8000/file_demo/register/', data=credentials, headers=header)
#     secure_cookie = web.cookies
#     print web.content[0:7000]
#     print web.status_code
#     web = requests.get('http://localhost:8000/file_demo/cookie_test/',cookies=secure_cookie)
#     #web = requests.get('http://localhost:8000/file_demo/cookie_test/')
#     print web.content

#Test associating file with users
# client = requests.session()
# client.get('http://localhost:8000/file_demo/login/')
# csrf = client.cookies['csrftoken']
# #print csrf
# credentials = {'username': 'test2', 'password':'password'}
# header = {'X-CSRFToken': csrf}
# web = client.post('http://localhost:8000/file_demo/login/', data=credentials, headers=header)
# secure_cookie = web.cookies
# #print web.cookies
# print web.content
# web = requests.get('http://localhost:8000/file_demo/cookie_test/',cookies=secure_cookie)
# print web.content
# directory = {'directory': 'myfiles/supersecret'}
# url = "http://localhost:8000/file_demo/upload_file/"
# response = requests.post(url,files={'file': open('test1.txt','rb')}, data=directory, cookies=secure_cookie)
# print response.content[0:7000]

#Test user password change
# client = requests.session()
# client.get('http://localhost:8000/file_demo/login/')
# #print client.cookies
# csrf = client.cookies['csrftoken']
# #print csrf
# credentials = {'username': 'test2', 'password':'newpassword'}
# header = {'X-CSRFToken': csrf}
# web = client.post('http://localhost:8000/file_demo/login/', data=credentials, headers=header)
# secure_cookie = web.cookies
# print web.cookies
# print web.content[0:7000]
#
# client2 = requests.session()
# client2.get('http://localhost:8000/file_demo/change_password/')
# print client2.cookies
# csrf2 = client2.cookies['csrftoken']
# secure_cookie['csrftoken'] = None
# header2 = {'X-CSRFToken': csrf2}
# credential2 = {'password': 'password'}
# web2 = client2.post('http://localhost:8000/file_demo/change_password/', data=credential2, headers=header2, cookies=secure_cookie)
# print web2.content[0:7000]
# print web2.status_code

#Test json request function
# client = requests.session()
# client.get('http://localhost:8000/file_demo/login/')
# csrf = client.cookies['csrftoken']
# #print csrf
# credentials = {'username': 'test4', 'password':'password'}
# header = {'X-CSRFToken': csrf}
# web = client.post('http://localhost:8000/file_demo/login/', data=credentials, headers=header)
# secure_cookie = web.cookies
# print web.cookies
# print web.content[0:7000]
# web = requests.get('http://localhost:8000/file_demo/json_request/',cookies=secure_cookie)
# #web = requests.get('http://localhost:8000/file_demo/json_request/')
# print web.content[0:7000]

#Test delete file function
# client = requests.session()
# client.get('http://localhost:8000/file_demo/login/')
# csrf = client.cookies['csrftoken']
# #print csrf
# credentials = {'username': 'test2', 'password':'password'}
# header = {'X-CSRFToken': csrf}
# web = client.post('http://localhost:8000/file_demo/login/', data=credentials, headers=header)
# secure_cookie = web.cookies
# # print web.cookies
# print web.content[0:7000]
# directory = {'directory': 'myfiles/supersecret', 'file': 'test1.txt'}
# web = requests.post('http://localhost:8000/file_demo/delete_file/', data=directory, cookies=secure_cookie)
# #web = requests.get('http://localhost:8000/file_demo/delete_file/', data=directory)
# print web.content[0:7000]

#TEST file download
client = requests.session()
client.get('http://localhost:8000/file_demo/login/')
csrf = client.cookies['csrftoken']
#print csrf
credentials = {'username': 'test2', 'password':'password'}
header = {'X-CSRFToken': csrf}
web = client.post('http://localhost:8000/file_demo/login/', data=credentials, headers=header)
secure_cookie = web.cookies
#print web.cookies
print web.content
web = requests.get('http://localhost:8000/file_demo/cookie_test/',cookies=secure_cookie)
print web.content
directory = {'directory': 'myfiles/supersecret', 'file': 'test1.txt'}
url = "http://localhost:8000/file_demo/download_file/"
response = requests.post(url, data=directory, cookies=secure_cookie)
print response.content[0:7000]
