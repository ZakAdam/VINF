import requests
import re

# URL of the web page you want to scrape
url = "https://kyivindependent.com/tag/war/"  # Replace with your desired URL

# Send an HTTP GET request to the URL
response = requests.get(url)

# Variable holding found links
links = []

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
    #article_pattern = r'<div class="c-content ">\n.*\n.*\n\n.*<div id="reading-progress-end">'
    article_pattern = r'<div class=\'c-content \'>.*<div id="reading-progress-end">'
    #article_pattern = r'c-content \'.*"reading-progress-end'
    h1_matches = re.findall(h1_pattern, html_content, re.DOTALL)
    article_matches = re.search(article_pattern, html_content, re.DOTALL)

    print(article_matches.group(0))
    #print(html_content.replace("\n", ''))
    print(h1_matches)

    exit(0)
