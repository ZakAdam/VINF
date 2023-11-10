import requests
import re
from libraries import csv_manager

url = 'https://www.kyivpost.com/post/'
df = csv_manager.load_data('data/data-post.csv')
error_count = 0
number_of_errors = 0
post_id = 22418 #1
limit = 100

h1_pattern = r'(<h1 class=\"post-title\">)(.*)</h1>'
article_pattern = r'(<div id=\"post-content\">)(.*)\n</section>'
date_pattern = r'<div class=\"post-info\">.*?(\w+ \d{1,2}, \d{4},\s+\d{1,2}:\d{2} [ap]m).*?</div>'
# remove patterns
script_pattern = r'<script.*?</script>'
picture_pattern = r'<picture.*?</picture>'
div_pattern = r'<div.*?<p'

while error_count < limit:

    try:
        response = requests.get(url + f'{post_id}')
    except requests.exceptions.RequestException as e:
        print(f"Request encountered an error: {e}")
        print(f'Error on id: {post_id}')
        number_of_errors += 1
        post_id += 1
        continue

    if response.status_code != 200:
        print(f'Error on post id: {post_id}')
        number_of_errors += 1
        error_count += 1
        post_id += 1
        continue

    error_count = 0
    html_content = response.text

    # Header
    h1_matches = re.search(h1_pattern, html_content, re.DOTALL)

    # Article
    article_matches = re.search(article_pattern, html_content, re.DOTALL)

    # Date
    date = re.search(date_pattern, html_content, re.DOTALL)

    #if date is None:
    #    date = None
    #else:
    #    date = date.group(1)

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

    removed_scripts = re.sub(script_pattern, '', article_matches.group(2).replace('\t', ' '), flags=re.DOTALL)
    removed_pictures = re.sub(picture_pattern, '', removed_scripts, flags=re.DOTALL)
    cleaned_html = re.sub(div_pattern, '', removed_pictures, flags=re.DOTALL)

    df.loc[len(df)] = [h1_matches.group(2).replace('\t', ' '),
                       url + f'{post_id}',
                       'Ukraine',
                       date.group(1),
                       cleaned_html]

    if post_id % 1000 == 0:
        csv_manager.store_data('data/data-post.csv', df)

    post_id += 1

csv_manager.store_data('data/data-post.csv', df)
