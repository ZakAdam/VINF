import requests
import re
from libraries import csv_manager

url = 'https://www.kyivpost.com/post/'
df = csv_manager.load_data('data/data-post.csv')
error_count = 0
number_of_errors = 0
post_id = 1
limit = 100

while error_count < limit:
    response = requests.get(url + f'{post_id}')

    if response.status_code != 200:
        print(f'Error on post id: {post_id}')
        number_of_errors += 1
        error_count += 1
        post_id += 1
        continue

    error_count = 0
    html_content = response.text

    # Header
    h1_pattern = r'(<h1 class=\"post-title\">)(.*)</h1>'
    h1_matches = re.search(h1_pattern, html_content, re.DOTALL)

    # Article
    article_pattern = r'(<div id=\"post-content\">)(.*)\n</section>'
    article_matches = re.search(article_pattern, html_content, re.DOTALL)

    if article_matches is None:
        print(f'Post with no article: {post_id}\n')
        post_id += 1
        continue

    print(post_id)
    print(h1_matches.group(2))
    print('\n')

    df.loc[len(df)] = [h1_matches.group(2).replace('\t', ' '),
                       url + f'{post_id}',
                       'Ukraine',
                       None,
                       article_matches.group(2).replace('\t', ' ')]

    if post_id % 1000 == 0:
        csv_manager.store_data('data/data-post.csv', df)

    post_id += 1

csv_manager.store_data('data/data-post.csv', df)
