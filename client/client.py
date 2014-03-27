import requests
#url = "http://localhost:8000/file_demo/upload_file/"
#response = requests.post(url,files={'file': open('test.txt','rb')})
client = requests.session()
client.get('http://localhost:8000/file_demo/login/')
csrf = client.cookies['csrftoken']
#print csrf
credentials = {'username': 'test1', 'password':'password'}
header = {'X-CSRFToken': csrf}
web = client.post('http://localhost:8000/file_demo/login/',data=credentials, headers=header)
secure_cookie = web.cookies
print web.content
print web.cookies
web = requests.get('http://localhost:8000/file_demo/cookie_test/',cookies=secure_cookie)
print web.content

