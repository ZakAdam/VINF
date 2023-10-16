import datetime
import requests
from libraries import load_links

url = 'https://tass.com/api/news/lenta?limit=200'

response = requests.get(url)
json_data = response.json()['articles']
current_date = json_data[-1]['time']
#links = {}
urls = []

#while len(links) < 30000:
while len(urls) < 30000:
    query = url + '&before=' + current_date
    response = requests.get(query)
    json_data = response.json()['articles']
    current_date = json_data[-1]['time']

    print_date = datetime.datetime.fromtimestamp(int(current_date)).strftime('%Y-%m-%d %H:%M:%S')
    print(f'Parsing articles before date: {print_date}')

    for article in json_data:
        #links[article['url']] = [article['title'], article['time']]
        urls.append('https://tass.com' + article['url'])

print('Ending links gathering, starting to store urls...')
load_links.store_links('data-tass.txt', urls)
