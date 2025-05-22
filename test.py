import requests

url = "http://127.0.0.1:5000/api/detect"
files = {'image': open('rice-blast-11_jpg.rf.34f94fb32d95584caa39cfa09086593d.jpg', 'rb')}
response = requests.post(url, files=files)
print(response.json())