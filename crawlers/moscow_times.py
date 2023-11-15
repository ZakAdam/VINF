import requests
import re
from libraries import load_links
from libraries import csv_manager

# URL of the web page you want to scrape
url = "https://www.themoscowtimes.com/ukraine-war/"

# Initialize the iterator
offset = 0
links = set()
processed_links = set()
page_count = 0
df = csv_manager.load_data('../data/data-moscow.csv')

# number of articles pre request: 18
# number of max offset -> 1914
#'''
while True:
    # Make a request (you should replace the URL with your actual request)
    url = f"https://www.themoscowtimes.com/ukraine-war/{offset}"
    response = requests.get(url)
    html_content = response.text

    # Check if the response is empty
    if not html_content:
        print(offset)
        print("Received an empty response. Stopping the loop.")
        break

    a_pattern = r'<a href=[\"\'](https://.+?)[\"\']'
    a_matches = set(re.findall(a_pattern, html_content, re.DOTALL))

    for link in a_matches:
        links.append(link)

    # Add 18 to the iterator for the next iteration
    print(offset)
    offset += 18

print('Starting storing data')
load_links.store_links('moscow-links.txt', links)
print('Links stored!')
#'''

load_links.load_links_stack('../moscow-links.txt', links)
#links_set = set(links)

#for link in links:
while len(links) > 0:
    link = next(iter(links))
    response = requests.get(link)

    if response.status_code != 200:
        print(f'Error on link: {link}')
        processed_links.add(link)
        links.remove(link)
        continue

    html_content = response.text

    # Header
    h1_pattern = r'(<header.*<h1><a href=.+>)(.*)</a>.*</h1>'
    h1_matches = re.search(h1_pattern, html_content, re.DOTALL)
    # Article
    article_pattern = r'y-name=\"article-content\">(.*)<div class=\"article__bottom\">'
    article_matches = re.search(article_pattern, html_content, re.DOTALL)

    if article_matches is None:
        print(f'Link with no article: {link}\n')
        processed_links.add(link)
        links.remove(link)
        continue

    date_pattern = r'/(\d{4}/\d{2}/\d{2})/'
    date_matches = re.search(date_pattern, link, re.DOTALL)

    if date_matches is not None:
        date_matches = date_matches.group(1)
    else:
        date_matches = None

    # Links
    href_pattern = r'<a\s+[^>]*href=[\"\']((https://).+?)[\"\']'
    article_links = re.findall(href_pattern, article_matches.group(1), re.DOTALL)

    print(page_count)
    print(h1_matches.group(2))
    print(f'Current links size is: {len(links)}')
    print('\n')

    df.loc[len(df)] = [h1_matches.group(2).replace('\t', ' '),
                       link,
                       'Russia',
                       date_matches,
                       article_matches.group(1).replace('\t', ' ')]

    processed_links.add(link)
    links.remove(link)

    for new_link in article_links:
        if 'themoscowtimes' in new_link and new_link not in processed_links:
            print(f'Link was added: {new_link}')
            links.add(new_link)

    page_count += 1

csv_manager.store_data('../data/data-moscow.csv', df)