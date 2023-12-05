import requests
import re
from libraries import csv_manager

# Script to scrape Kyiv Post webiste
url = 'https://www.kyivpost.com/post/'
df = csv_manager.load_data('../data/data-post.csv')
error_count = 0
number_of_errors = 0
# Starting Post id to scrape. When 1 is given we scrape for beginning.
post_id = 1     # 22418
limit = 100

# Search RegEx patterns
h1_pattern = r'(<h1 class=\"post-title\">)(.*)</h1>'
article_pattern = r'(<div id=\"post-content\">)(.*)\n</section>'
date_pattern = r'<div class=\"post-info\">.*?(\w+ \d{1,2}, \d{4},\s+\d{1,2}:\d{2} [ap]m).*?</div>'
# Remove RegEx patterns
script_pattern = r'<script.*?</script>'
picture_pattern = r'<picture.*?</picture>'
div_pattern = r'<div.*?<p'

# Loop until we are getting multiple errors in row. This means we are at the end posts.
while error_count < limit:
    try:
        response = requests.get(url + f'{post_id}')
    except requests.exceptions.RequestException as e:
        print(f"Request encountered an error: {e}")
        print(f'Error on id: {post_id}')
        number_of_errors += 1                       # Increase number of errors
        post_id += 1                                # Increase to another post ID
        continue

    if response.status_code != 200:
        print(f'Error on post id: {post_id}')
        number_of_errors += 1                       # Increase number of errors
        error_count += 1                            # Increase error count -> We get 404 wrong URL
        post_id += 1                                # Increase to another post ID
        continue

    # If request was successful reset error count
    error_count = 0
    html_content = response.text

    # Header
    h1_matches = re.search(h1_pattern, html_content, re.DOTALL)

    # Article
    article_matches = re.search(article_pattern, html_content, re.DOTALL)

    # Date
    date = re.search(date_pattern, html_content, re.DOTALL)

    if article_matches is None:
        print(f'Post with no article: {post_id}\n')
        post_id += 1
        continue

    if date is None:
        print(f'Post with no date: {post_id}\n')
        post_id += 1
        continue

    print(post_id)
    print(h1_matches.group(2))
    print('\n')

    # Remove useless tags defined above, such as <script> etc.
    removed_scripts = re.sub(script_pattern, '', article_matches.group(2).replace('\t', ' '), flags=re.DOTALL)
    removed_pictures = re.sub(picture_pattern, '', removed_scripts, flags=re.DOTALL)
    cleaned_html = re.sub(div_pattern, '', removed_pictures, flags=re.DOTALL)

    # Add new data to dataframe
    df.loc[len(df)] = [h1_matches.group(2).replace('\t', ' '),
                       url + f'{post_id}',
                       'Ukraine',
                       date.group(1),
                       cleaned_html]

    # Every N iteration save links to CSV
    if post_id % 1000 == 0:
        csv_manager.store_data('../data/data-post.csv', df)

    post_id += 1

# After all links are processed, store rest of the data
csv_manager.store_data('../data/data-post.csv', df)
