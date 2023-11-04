import datetime
import requests
import re
from libraries import csv_manager

url = 'https://tass.com/api/news/lenta?limit=200'

response = requests.get(url)
json_data = response.json()['articles']
current_date = json_data[-1]['time']
links = {}

while len(links) < 40000:
    query = url + '&before=' + current_date
    response = requests.get(query)
    json_data = response.json()['articles']
    current_date = json_data[-1]['time']

    print_date = datetime.datetime.fromtimestamp(int(current_date)).strftime('%Y-%m-%d %H:%M:%S')
    print(f'Parsing articles before date: {print_date}')

    for article in json_data:
        links[article['url']] = [article['title'], article['time']]

    print(f'Len of links: {len(links)}')

print('Ending links gathering, starting to store crawl links...')

iterator = 0
df = csv_manager.load_data('data/data-tass.csv')

while len(links) > 0:
    post_url = next(iter(links))
    post_title = links[post_url][0]
    post_datetime = links[post_url][1]
    link = 'https://tass.com' + post_url

    try:
        response = requests.get(link)
    except requests.exceptions.RequestException as e:
        print(f"Request encountered an error: {e}")
        print(f'Error on link: {link}')
        del links[post_url]
        iterator += 1
        continue

    if response.status_code != 200:
        print(f'Error on link: {link}')
        del links[post_url]
        iterator += 1
        continue

    html_content = response.text

    # Article
    article_pattern = r'(<div class=\"text-content\">)(.*)<div class=\"column\">'
    article_matches = re.search(article_pattern, html_content, re.DOTALL)

    if article_matches is None:
        print(f'Post with no article: {post_url}\n')
        del links[post_url]
        iterator += 1
        continue

    print(iterator)
    print(post_url)
    print(post_title)
    print(post_datetime)
    print(f'Current links size is: {len(links)}')
    print('\n')

    df.loc[len(df)] = [post_title.replace('\t', ' '),
                       link,
                       'Russia',
                       post_datetime,
                       article_matches.group(2).replace('\t', ' ')]

    if iterator % 1000 == 0:
        csv_manager.store_data('data/data-tass.csv', df)

    del links[post_url]
    iterator += 1

print('End of crawling, starting last save...')
csv_manager.store_data('data/data-tass.csv', df)
print('Done!')
