import requests

#Test file upload
#url = "http://localhost:8000/file_demo/upload_file/"
#response = requests.post(url,files={'file': open('test.txt','rb')})

#test user login
client = requests.session()
client.get('http://localhost:8000/file_demo/login/')
csrf = client.cookies['csrftoken']
#print csrf
credentials = {'username': 'test1', 'password':'password'}
header = {'X-CSRFToken': csrf}
e_demo/cookie_test/')
web = requests.get('http://localhost:8000/file_demo/cookie_test/',cookies=secure_cookie)
print web.content

