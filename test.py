import requests

url = 'https://www.kyivpost.com/post/'

response = requests.get(url + '22721')

print(response.status_code)
print(response.text)
