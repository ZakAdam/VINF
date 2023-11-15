import requests
import re
from libraries import load_links, csv_manager


class MoscowTimesCrawler:
    def __init__(self, start_url='https://www.themoscowtimes.com/ukraine-war/', csv_path='../data/data-moscow.csv'):
        self.url = start_url
        self.csv_path = csv_path
        self.offset = 0
        self.links = set()
        self.processed_links = set()
        self.page_count = 0
        self.df = csv_manager.load_data(csv_path)

    def scrape_links(self):
        while True:
            url = f"{self.url}/{self.offset}"
            response = requests.get(url)
            html_content = response.text

            if not html_content:
                print(self.offset)
                print("Received an empty response. Stopping the loop.")
                break

            a_pattern = r'<a href=[\"\'](https://.+?)[\"\']'
            a_matches = set(re.findall(a_pattern, html_content, re.DOTALL))

            for link in a_matches:
                self.links.add(link)

            print(self.offset)
            self.offset += 18

        print('Starting storing data')
        load_links.store_links('moscow-links.txt', self.links)
        print('Links stored!')

    def crawl_and_store_data(self):
        load_links.load_links_stack('moscow-links.txt', self.links)

        while len(self.links) > 0:
            link = next(iter(self.links))
            response = requests.get(link)

            if response.status_code != 200:
                print(f'Error on link: {link}')
                self.processed_links.add(link)
                self.links.remove(link)
                continue

            html_content = response.text

            h1_pattern = r'(<header.*<h1><a href=.+>)(.*)</a>.*</h1>'
            h1_matches = re.search(h1_pattern, html_content, re.DOTALL)

            article_pattern = r'y-name=\"article-content\">(.*)<div class=\"article__bottom\">'
            article_matches = re.search(article_pattern, html_content, re.DOTALL)

            if article_matches is None:
                print(f'Link with no article: {link}\n')
                self.processed_links.add(link)
                self.links.remove(link)
                continue

            date_pattern = r'/(\d{4}/\d{2}/\d{2})/'
            date_matches = re.search(date_pattern, link, re.DOTALL)

            if date_matches is not None:
                date_matches = date_matches.group(1)
            else:
                date_matches = None

            href_pattern = r'<a\s+[^>]*href=[\"\']((https://).+?)[\"\']'
            article_links = re.findall(href_pattern, article_matches.group(1), re.DOTALL)

            print(self.page_count)
            print(h1_matches.group(2))
            print(f'Current links size is: {len(self.links)}')
            print('\n')

            self.df.loc[len(self.df)] = [h1_matches.group(2).replace('\t', ' '),
                                         link,
                                         'Russia',
                                         date_matches,
                                         article_matches.group(1).replace('\t', ' ')]

            self.processed_links.add(link)
            self.links.remove(link)

            for new_link in article_links:
                if 'themoscowtimes' in new_link and new_link not in self.processed_links:
                    print(f'Link was added: {new_link}')
                    self.links.add(new_link)

            self.page_count += 1

        csv_manager.store_data(self.csv_path, self.df)
        print('Done!')


# Example usage
if __name__ == "__main__":
    crawler = MoscowTimesCrawler()
    crawler.scrape_links()
    crawler.crawl_and_store_data()
