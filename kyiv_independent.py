import requests
import re


def manage_links(rm_link, new_links, save_iterator, limit=10):
    processed_links_to_write.append(rm_link)
    save_iterator += 1

    for new_link in new_links:
        if new_link not in processed_links:
            links.append(new_link)
            unprocessed_links_to_write.append(new_link)

    if save_iterator >= limit:
        for writable_link in processed_links_to_write:
            processed_links_stack.write(writable_link + '\n')

        for writable_link in unprocessed_links_to_write:
            links_stack.write(writable_link + '\n')

        save_iterator = 0
        processed_links_to_write.clear()
        unprocessed_links_to_write.clear()

    links.pop()
    links.extend(new_links)


# URL of the web page you want to scrape
url = "https://kyivindependent.com/tag/war/"  # Replace with your desired URL

# Send an HTTP GET request to the URL
response = requests.get(url)

# Variable holding found links
links = []
processed_links = set()
processed_links_to_write = []
unprocessed_links_to_write = []
links_stack = open('independent_stack.txt', 'a+')
processed_links_stack = open('independent_processed.txt', 'a+')
save_iterator = 0

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
            break

    for href in links:
        print(href)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Start scraping websites
for link in links:
    response = requests.get(link)

    if response.status_code != 200:
        continue

    html_content = response.text

    # Header
    h1_pattern = r'<h1[^>]*>.*?</h1>'
    h1_matches = re.search(h1_pattern, html_content, re.DOTALL)
    # Article
    article_pattern = r'<div class=\'c-content \'>.*<div id="reading-progress-end">'
    article_matches = re.search(article_pattern, html_content, re.DOTALL)
    # Links
    href_pattern = r'href=["\'](https?://[^"\']+)["\']'
    article_links = re.findall(href_pattern, article_matches.group(0), re.DOTALL)

    print(article_matches.group(0))
    print(h1_matches.group(0))
    print(article_links)

    manage_links(link, article_links, save_iterator, 1)

    exit(0)
