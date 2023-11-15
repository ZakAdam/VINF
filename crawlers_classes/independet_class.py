import requests
import re
from libraries import load_links, csv_manager


class IndependentCrawler:
    def __init__(self, urls, csv_path='../data/data-tags.csv'):
        self.urls_to_scrape = ['https://kyivindependent.com/tag/war/', 'https://kyivindependent.com/tag/opinion/',
                               'https://kyivindependent.com/tag/business/',
                               'https://kyivindependent.com/tag/eastern-europe/',
                               'https://kyivindependent.com/tag/culture/',
                               'https://kyivindependent.com/tag/investigations/',
                               'https://kyivindependent.com/tag/war-analysis/',
                               'https://kyivindependent.com/tag/human-story/',
                               'https://kyivindependent.com/tag/national/',
                               'https://kyivindependent.com/tag/field-report/',
                               'https://kyivindependent.com/tag/russias-war/',
                               'https://kyivindependent.com/tag/company-news/']
        self.urls = urls
        self.csv_path = csv_path
        self.links = set()
        self.processed_links = set()
        self.processed_links_to_write = []
        self.unprocessed_links_to_write = []
        self.links_stack = open('independent_stack.txt', 'a+')
        self.processed_links_stack = open('independent_processed.txt', 'a+')
        self.save_iterator = 0
        self.df = csv_manager.load_data(csv_path)
        self.page_count = 0

    def manage_links(self, rm_link, new_links, iterator, limit=10):
        self.processed_links.add(rm_link)
        self.processed_links_to_write.append(rm_link)
        iterator += 1

        for new_link in new_links:
            if (new_link not in self.processed_links
                    and new_link.startswith('https://kyivindependent.com/')
                    and '/ghost/#/' not in new_link):
                self.links.add(new_link)
                self.unprocessed_links_to_write.append(new_link)

        if iterator >= limit:
            print('Started storing data to files...')
            csv_manager.store_data(self.csv_path, self.df)

            for writable_link in self.processed_links_to_write:
                self.processed_links_stack.write(writable_link + '\n')

            for writable_link in self.unprocessed_links_to_write:
                self.links_stack.write(writable_link + '\n')

            iterator = 0
            self.processed_links_to_write.clear()
            self.unprocessed_links_to_write.clear()
            print('Ended file storing.')

        self.links.remove(rm_link)

        return iterator

    def scrape_links(self):
        for url in self.urls:
            response = requests.get(url)

            if response.status_code == 200:
                html_content = response.text
                h3_pattern = r'<h3[^>]*>.*?</h3>'
                a_pattern = r'<a\s+[^>]*href=["\']((?!https://).+?)["\']'

                h3_matches = re.findall(h3_pattern, html_content, re.DOTALL)

                for h3_match in h3_matches:
                    a_matches = re.search(a_pattern, h3_match)
                    if a_matches is not None:
                        self.links.add('https://kyivindependent.com' + str(a_matches.group(1)))
                        # break

                print(f'Starting links size: {len(self.links)}')

            else:
                print(f"Failed to retrieve the page. Status code: {response.status_code}")

    def crawl_and_store_data(self):
        load_links.load_processed_links('independent_processed.txt', self.processed_links)
        load_links.load_links_stack('independent_stack.txt', self.links)

        while len(self.links) > 0:
            link = next(iter(self.links))
            response = requests.get(link)
            print(link)

            if response.status_code != 200:
                print(f'Error on link: {link}')
                self.processed_links.add(link)
                self.links.remove(link)
                continue

            html_content = response.text
            h1_pattern = r'<(h1|h2)[^>]*>.*?</(h1|h2)>'
            h1_matches = re.search(h1_pattern, html_content, re.DOTALL)

            article_pattern = r'<div class=\'c-content \'>.*<div id="reading-progress-end">'
            article_matches = re.search(article_pattern, html_content, re.DOTALL)

            if article_matches is None:
                print(f'Link with no article: {link}')
                self.processed_links.add(link)
                self.links.remove(link)
                continue

            date_pattern = r'(\w+ \d{1,2}, \d{4} \d{1,2}:\d{2} [APap][Mm])'
            date_matches = re.search(date_pattern, html_content, re.DOTALL)
            if date_matches is not None:
                date_matches = date_matches.group(0)
            else:
                date_matches = None

            href_pattern = r'href=["\'](https?://[^"\']+)["\']'
            article_links = re.findall(href_pattern, html_content, re.DOTALL)

            print(self.page_count)
            print(h1_matches.group(0))
            print(f'Current links size is: {len(self.links)}')
            print('\n')

            self.df.loc[len(self.df)] = [str(h1_matches.group(0).replace('\t', ' ')),
                                         link,
                                         'Ukraine',
                                         date_matches,
                                         article_matches.group(0).replace('\t', ' ')]

            self.save_iterator = self.manage_links(link, article_links, self.save_iterator, limit=1000)

            self.page_count += 1

        print('Started storing data to files...')
        csv_manager.store_data(self.csv_path, self.df)

        for writable_link in self.processed_links_to_write:
            self.processed_links_stack.write(writable_link + '\n')

        for writable_link in self.unprocessed_links_to_write:
            self.links_stack.write(writable_link + '\n')

        self.save_iterator = 0
        self.processed_links_to_write.clear()
        self.unprocessed_links_to_write.clear()
        print('Ended file storing.')


if __name__ == "__main__":
    crawler = IndependentCrawler()
    crawler.scrape_links()
    crawler.crawl_and_store_data()
