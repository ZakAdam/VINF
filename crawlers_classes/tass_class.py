import datetime
import requests
import re
from libraries import csv_manager


class TassCrawler:
    def __init__(self, url='https://tass.com/api/news/lenta?limit=200', csv_path='../data/data-tass.csv', limit=40000):
        self.url = url
        self.csv_path = csv_path
        self.limit = limit
        self.links = {}
        self.iterator = 0
        self.df = csv_manager.load_data(csv_path)

    def gather_links(self):
        response = requests.get(self.url)
        json_data = response.json()['articles']
        current_date = json_data[-1]['time']

        while len(self.links) < self.limit:
            query = self.url + '&before=' + current_date
            response = requests.get(query)
            json_data = response.json()['articles']
            current_date = json_data[-1]['time']

            print_date = datetime.datetime.fromtimestamp(int(current_date)).strftime('%Y-%m-%d %H:%M:%S')
            print(f'Parsing articles before date: {print_date}')

            for article in json_data:
                self.links[article['url']] = [article['title'], article['time']]

            print(f'Len of links: {len(self.links)}')

        print('Ending links gathering, starting to store crawl links...')

    def crawl_and_store_data(self):
        while len(self.links) > 0:
            post_url = next(iter(self.links))
            post_title = self.links[post_url][0]
            post_datetime = self.links[post_url][1]
            link = 'https://tass.com' + post_url

            try:
                response = requests.get(link)
            except requests.exceptions.RequestException as e:
                print(f"Request encountered an error: {e}")
                print(f'Error on link: {link}')
                del self.links[post_url]
                self.iterator += 1
                continue

            if response.status_code != 200:
                print(f'Error on link: {link}')
                del self.links[post_url]
                self.iterator += 1
                continue

            html_content = response.text

            # Article
            article_pattern = r'(<div class=\"text-content\">)(.*)<div class=\"column\">'
            article_matches = re.search(article_pattern, html_content, re.DOTALL)

            if article_matches is None:
                print(f'Post with no article: {post_url}\n')
                del self.links[post_url]
                self.iterator += 1
                continue

            print(self.iterator)
            print(post_url)
            print(post_title)
            print(post_datetime)
            print(f'Current links size is: {len(self.links)}')
            print('\n')

            self.df.loc[len(self.df)] = [post_title.replace('\t', ' '),
                                         link,
                                         'Russia',
                                         post_datetime,
                                         article_matches.group(2).replace('\t', ' ')]

            if self.iterator % 1000 == 0:
                csv_manager.store_data(self.csv_path, self.df)

            del self.links[post_url]
            self.iterator += 1

        print('End of crawling, starting last save...')
        csv_manager.store_data(self.csv_path, self.df)
        print('Done!')


# Example usage
if __name__ == "__main__":
    crawler = TassCrawler()
    crawler.gather_links()
    crawler.crawl_and_store_data()
