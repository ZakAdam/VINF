import pandas as pd
import requests
import re
from libraries import load_links
from libraries import csv_manager


def manage_links(rm_link, new_links, iterator, limit=10):
    processed_links_to_write.append(rm_link)
    iterator += 1

    for new_link in new_links:
        if new_link not in processed_links and 'kyivindependent' in new_link:
            links.append(new_link)
            unprocessed_links_to_write.append(new_link)

    if iterator >= limit:
        print('Started storing data to files...')
        csv_manager.store_data('data.csv', df)

        for writable_link in processed_links_to_write:
            processed_links_stack.write(writable_link + '\n')

        for writable_link in unprocessed_links_to_write:
            links_stack.write(writable_link + '\n')

        iterator = 0
        processed_links_to_write.clear()
        unprocessed_links_to_write.clear()
        print('Ended file storing.')

    links.pop()

    return iterator


# Variable holding found links
links = []
processed_links = set()
processed_links_to_write = []
unprocessed_links_to_write = []
links_stack = open('independent_stack.txt', 'a+')
processed_links_stack = open('independent_processed.txt', 'a+')
save_iterator = 0
df = csv_manager.load_data('data.csv')
page_count = 0


# URL of the web page you want to scrape
url = "https://kyivindependent.com/tag/war/"  # Replace with your desired URL
# Send an HTTP GET request to the URL
response = requests.get(url)

load_links.load_processed_links('independent_processed.txt', processed_links)
load_links.load_links_stack('independent_stack.txt', links)

# Check if the request was successful
if response.status_code == 200:
    # Get the HTML content of the page
    html_content = response.text

    # Define regex patterns for finding <h3> elements and nested <a> tags
    h3_pattern = r'<h3[^>]*>.*?</h3>'
    a_pattern = r'<a\s+[^>]*href=["\']((?!https://).+?)["\']'

    # Find <h3> elements using regex
    h3_matches = re.findall(h3_pattern, html_content, re.DOTALL)

    for h3_match in h3_matches:
        # Search for nested <a> tags within the <h3> element
        a_matches = re.search(a_pattern, h3_match)
        if a_matches is not None:
            links.append('https://kyivindependent.com' + str(a_matches.group(1)))
            # break

    for href in links:
        print(href)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Start scraping websites
for link in links:
    response = requests.get(link)
    print(link)

    if response.status_code != 200:
        print(f'Error on link: {link}')
        continue

    html_content = response.text

    # Header
    h1_pattern = r'<(h1|h2)[^>]*>.*?</(h1|h2)>'
    h1_matches = re.search(h1_pattern, html_content, re.DOTALL)
    # Article
    article_pattern = r'<div class=\'c-content \'>.*<div id="reading-progress-end">'
    article_matches = re.search(article_pattern, html_content, re.DOTALL)

    if article_matches.group(0) is None:
        print(f'Link with no article: {link}')
        continue
    # Links
    href_pattern = r'href=["\'](https?://[^"\']+)["\']'
    article_links = re.findall(href_pattern, article_matches.group(0), re.DOTALL)

    #print(article_matches.group(0))
    print(page_count)
    print(h1_matches.group(0))
    print('\n')
    #print(article_links)

    df.loc[len(df)] = [str(h1_matches.group(0).replace('\t', ' ')), link, 'Ukraine', article_matches.group(0).replace('\t', ' ')]
    save_iterator = manage_links(link, article_links, save_iterator, limit=50)

    page_count += 1
    # exit(0)

# Store the last values, after all links are processed
manage_links('https://kyivindependent.com/tag/war/', [], 1000000000)
