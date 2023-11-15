import requests
import re
from libraries import csv_manager


class PostScraper:
    def __init__(self, url='https://www.kyivpost.com/post/', csv_path='../data/data-post.csv', limit=100,
                 start_post_id=0):
        self.url = url
        self.csv_path = csv_path
        self.limit = limit
        self.start_post_id = start_post_id
        self.df = csv_manager.load_data(csv_path)
        self.error_count = 0
        self.number_of_errors = 0

        self.h1_pattern = r'(<h1 class=\"post-title\">)(.*)</h1>'
        self.article_pattern = r'(<div id=\"post-content\">)(.*)\n</section>'
        self.date_pattern = r'<div class=\"post-info\">.*?(\w+ \d{1,2}, \d{4},\s+\d{1,2}:\d{2} [ap]m).*?</div>'
        self.script_pattern = r'<script.*?</script>'
        self.picture_pattern = r'<picture.*?</picture>'
        self.div_pattern = r'<div.*?<p'

    def scrape_and_store_data(self):
        post_id = self.start_post_id

        while self.error_count < self.limit:
            try:
                response = requests.get(self.url + f'{post_id}')
            except requests.exceptions.RequestException as e:
                print(f"Request encountered an error: {e}")
                print(f'Error on id: {post_id}')
                self.number_of_errors += 1
                post_id += 1
                continue

            if response.status_code != 200:
                print(f'Error on post id: {post_id}')
                self.number_of_errors += 1
                self.error_count += 1
                post_id += 1
                continue

            self.error_count = 0
            html_content = response.text

            h1_matches = re.search(self.h1_pattern, html_content, re.DOTALL)
            article_matches = re.search(self.article_pattern, html_content, re.DOTALL)
            date = re.search(self.date_pattern, html_content, re.DOTALL)

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

            removed_scripts = re.sub(self.script_pattern, '', article_matches.group(2).replace('\t', ' '),
                                     flags=re.DOTALL)
            removed_pictures = re.sub(self.picture_pattern, '', removed_scripts, flags=re.DOTALL)
            cleaned_html = re.sub(self.div_pattern, '', removed_pictures, flags=re.DOTALL)

            self.df.loc[len(self.df)] = [h1_matches.group(2).replace('\t', ' '),
                                         self.url + f'{post_id}',
                                         'Ukraine',
                                         date.group(1),
                                         cleaned_html]

            if post_id % 1000 == 0:
                csv_manager.store_data(self.csv_path, self.df)

            post_id += 1

        csv_manager.store_data(self.csv_path, self.df)


# Example usage
if __name__ == "__main__":
    scraper = PostScraper()
    scraper.scrape_and_store_data()
