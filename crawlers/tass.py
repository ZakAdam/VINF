import datetime
import requests
import re
from libraries import csv_manager

# TASS API request to get links
url = 'https://tass.com/api/news/lenta?limit=200'

response = requests.get(url)
json_data = response.json()['articles']         # Load JSON respons
current_date = json_data[-1]['time']            # Load last date from reponse
links = {}

# Iterate over, until we have enough links
while len(links) < 40000:
    query = url + '&before=' + current_date         # Crete new request starting from last date
    response = requests.get(query)
    json_data = response.json()['articles']         # Load article data from JSON
    current_date = json_data[-1]['time']            # Load last datetime received

    print_date = datetime.datetime.fromtimestamp(int(current_date)).strftime('%Y-%m-%d %H:%M:%S')
    print(f'Parsing articles before date: {print_date}')

    # Add article data to array
    for article in json_data:
        links[article['url']] = [article['title'], article['time']]

    print(f'Len of links: {len(links)}')

print('Ending links gathering, starting to store crawl links...')

iterator = 0
df = csv_manager.load_data('../data/data-tass.csv')

# Iterate until we have processed all links
while len(links) > 0:
    post_url = next(iter(links))
    post_title = links[post_url][0]             # Load page title
    post_datetime = links[post_url][1]          # load page datetime
    link = 'https://tass.com' + post_url        # Create link from data

    try:
        response = requests.get(link)
    except requests.exceptions.RequestException as e:
        print(f"Request encountered an error: {e}")
        print(f'Error on link: {link}')
        del links[post_url]                     # Remove link from dictionary
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

    # Put processed data to dataframe
    df.loc[len(df)] = [post_title.replace('\t', ' '),
                       link,
                       'Russia',
                       post_datetime,
                       article_matches.group(2).replace('\t', ' ')]

    # After given number of iteration store data
    if iterator % 1000 == 0:
        csv_manager.store_data('../data/data-tass.csv', df)

    del links[post_url]
    iterator += 1

print('End of crawling, starting last save...')
csv_manager.store_data('../data/data-tass.csv', df)
print('Done!')
