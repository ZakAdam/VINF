import requests
import re
from libraries import load_links
from libraries import csv_manager


def manage_links(rm_link, new_links, iterator, limit=10):
    processed_links.add(rm_link)
    processed_links_to_write.append(rm_link)
    iterator += 1

    for new_link in new_links:
        if (new_link not in processed_links
                and new_link.startswith('https://kyivindependent.com/')
                and '/ghost/#/' not in new_link):
            links.add(new_link)
            unprocessed_links_to_write.append(new_link)

    if iterator >= limit:
        print('Started storing data to files...')
        # csv_manager.store_data('data_old.csv', df)
        csv_manager.store_data('data/data-tags.csv', df)

        for writable_link in processed_links_to_write:
            processed_links_stack.write(writable_link + '\n')

        for writable_link in unprocessed_links_to_write:
            links_stack.write(writable_link + '\n')

        iterator = 0
        processed_links_to_write.clear()
        unprocessed_links_to_write.clear()
        print('Ended file storing.')

    links.remove(rm_link)

    return iterator


# Variable holding found links
links = set()
processed_links = set()
processed_links_to_write = []
unprocessed_links_to_write = []
links_stack = open('independent_stack.txt', 'a+')
processed_links_stack = open('independent_processed.txt', 'a+')
save_iterator = 0
# df = csv_manager.load_data('data_old.csv')
df = csv_manager.load_data('data/data-tags.csv')
page_count = 0

load_links.load_processed_links('independent_processed.txt', processed_links)
load_links.load_links_stack('independent_stack.txt', links)

# URL of the web page you want to scrape
# url = "https://kyivindependent.com/tag/war/"
urls = ['https://kyivindependent.com/tag/war/', 'https://kyivindependent.com/tag/opinion/',
        'https://kyivindependent.com/tag/business/', 'https://kyivindependent.com/tag/eastern-europe/',
        'https://kyivindependent.com/tag/culture/', 'https://kyivindependent.com/tag/investigations/',
        'https://kyivindependent.com/tag/war-analysis/', 'https://kyivindependent.com/tag/human-story/',
        'https://kyivindependent.com/tag/national/', 'https://kyivindependent.com/tag/field-report/',
        'https://kyivindependent.com/tag/russias-war/', 'https://kyivindependent.com/tag/company-news/']

for url in urls:
    # Send an HTTP GET request to the URL
    response = requests.get(url)

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
                links.add('https://kyivindependent.com' + str(a_matches.group(1)))
                # break

        print(f'Starting links size: {len(links)}')

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Start scraping websites
# for link in links:
while len(links) > 0:
    link = next(iter(links))
    response = requests.get(link)
    print(link)

    if response.status_code != 200:
        print(f'Error on link: {link}')
        processed_links.add(link)
        links.remove(link)
        continue

    html_content = response.text

    # Header
    h1_pattern = r'<(h1|h2)[^>]*>.*?</(h1|h2)>'
    h1_matches = re.search(h1_pattern, html_content, re.DOTALL)

    # Article
    article_pattern = r'<div class=\'c-content \'>.*<div id="reading-progress-end">'
    article_matches = re.search(article_pattern, html_content, re.DOTALL)

    if article_matches is None:
        print(f'Link with no article: {link}')
        processed_links.add(link)
        links.remove(link)
        continue

    '''
    if h1_matches is None:
        print(f'Link with no article: {link}')
        processed_links.add(link)
        links.remove(link)
        continue
    '''

    date_pattern = r'(\w+ \d{1,2}, \d{4} \d{1,2}:\d{2} [APap][Mm])'
    date_matches = re.search(date_pattern, html_content, re.DOTALL)
    if date_matches is not None:
        date_matches = date_matches.group(0)
    else:
        date_matches = None

    # Links
    href_pattern = r'href=["\'](https?://[^"\']+)["\']'
    # article_links = re.findall(href_pattern, article_matches.group(0), re.DOTALL)
    article_links = re.findall(href_pattern, html_content, re.DOTALL)

    print(page_count)
    print(h1_matches.group(0))
    print(f'Current links size is: {len(links)}')
    print('\n')

    df.loc[len(df)] = [str(h1_matches.group(0).replace('\t', ' ')),
                       link,
                       'Ukraine',
                       date_matches,
                       article_matches.group(0).replace('\t', ' ')]

    '''
    df.loc[len(df)] = [str(h1_matches.group(0).replace('\t', ' ')),
                       link,
                       'Ukraine',
                       date_matches,
                       html_content.replace('\t', ' ')]
    '''

    save_iterator = manage_links(link, article_links, save_iterator, limit=1000)

    page_count += 1
    # exit(0)

# Store the last values, after all links are processed
# manage_links('https://kyivindependent.com/tag/war/', [], 1000000000)

print('Started storing data to files...')
# csv_manager.store_data('data_old.csv', df)
csv_manager.store_data('data/data-tags.csv', df)

for writable_link in processed_links_to_write:
    processed_links_stack.write(writable_link + '\n')

for writable_link in unprocessed_links_to_write:
    links_stack.write(writable_link + '\n')

iterator = 0
processed_links_to_write.clear()
unprocessed_links_to_write.clear()
print('Ended file storing.')
exit(0)
