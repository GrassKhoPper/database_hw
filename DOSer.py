import requests
import urllib3

urllib3.disable_warnings()

url = 'https://127.0.0.1:5000/'
headers = {
	'User-Agent': 'python-doser',
}

REQUEST_COUNT = 101

for _ in range(REQUEST_COUNT):
	x = requests.get(url=url, headers=headers, verify=False)
	print(x.status_code)

