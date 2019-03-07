import requests

url_base = 'http://127.0.0.1:5000/api/chainsaw'

dave_data = {'name': 'Dave', 'catches': 12, 'country': 'USA'}
response = requests.post(url_base, data=dave_data)
if response.status_code == requests.codes.created:
    print('Dave record created')
else:
    response.raise_for_status()

zoe_data = {'name': 'Zoe', 'catches': 42, 'country': 'Canada'}
response = requests.post(url_base, data=zoe_data)
if response.status_code == requests.codes.created:
    print('Zoe record created')
else:
    response.raise_for_status()


response = requests.get(url_base)
print(response.json(), response.status_code)
if response.status_code == requests.codes.ok:
    data = response.json()
    for index, record in enumerate(data):
        print(index, record)
else:
    response.raise_for_status()

updates = {'catches': 61}
response = requests.patch(f'{url_base}/1', data=updates)
if response.status_code == requests.codes.ok:
    print('Updated record 1')
else:
    response.raise_for_status()

response = requests.get(f'{url_base}/1')
if response.status_code == requests.codes.ok:
    print(response.json())
if response.status_code == requests.codes.not_found:
    print('Record 1 not found')
