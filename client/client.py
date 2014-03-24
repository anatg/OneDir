import requests
url = "http://localhost:8000/file_demo/upload_file/"
response = requests.post(url,files={'file': open('test.txt','rb')})
