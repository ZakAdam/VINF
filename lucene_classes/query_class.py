# Import necessary modules
from colorama import Fore, Style  # for colored terminal output
import textwrap                   # for wrapping text
import shutil                     # for getting terminal width

import lucene
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.index import DirectoryReader
from java.nio.file import Paths

# Define a class for Lucene search functionality
class LuceneSearcher:
    def __init__(self, index_dir='index', max_results=10, show_content=False, test_env=False):
        # Initialize LuceneSearcher with default parameters
        self.index_dir = index_dir
        self.max_results = max_results
        self.show_content = show_content
        self.index = MMapDirectory(Paths.get(index_dir))    # Lucene index directory
        self.searcher = IndexSearcher(DirectoryReader.open(self.index))  # Lucene IndexSearcher
        self.analyzer = StandardAnalyzer()                  # Lucene standard text analyzer
        self.ukraine_pages = []                             # List to store search results for Ukraine
        self.russian_pages = []                             # List to store search results for Russia
        self.test_env = test_env
        self.terminal_width = shutil.get_terminal_size()[0] - 2     # Get terminal width

    def query_string(self, query_str='Russia', date_search=False):
        # Method to perform a Lucene search given a query string and optional date search
        if not query_str:
            print('Empty string is not valid input')
            return

        if date_search:
            query_parser = QueryParser("date", self.analyzer)
        else:
            query_parser = QueryParser("content", self.analyzer)

        # Perform search for both Ukraine and Russia
        self.search_by_country(query_str, 'Ukraine', self.ukraine_pages, query_parser)
        self.search_by_country(query_str, 'Russia', self.russian_pages, query_parser)

        if not self.test_env:
            self.print_results()
        else:
            return {'UKR': self.ukraine_pages, 'RUS': self.russian_pages}

    def search_by_country(self, query_str, country, pages_dict, query_parser):
        # Method to perform country-specific Lucene search
        index_reader = DirectoryReader.open(self.index)
        searcher = IndexSearcher(index_reader)

        # Construct a query with both the input string and the country filter
        query_string = f'({query_str}) AND country:{country}'
        query = query_parser.parse(query_string)
        hits = searcher.search(query, self.max_results)

        # Populate the pages_dict list with search results
        for hit in hits.scoreDocs:
            doc = searcher.doc(hit.doc)
            pages_dict.append({'link': doc.get("link"),
                               'title': doc.get("title"),
                               'country': doc.get("country"),
                               'content': doc.get('content'),
                               'date': doc.get("date"),
                               'wiki_data': doc.get('Wiki Events')})

        # Close the index reader
        index_reader.close()

    def print_results(self):
        # Method to print search results in a formatted manner
        if not self.ukraine_pages and not self.russian_pages:
            print(Fore.YELLOW + 'No results found for this query!' + Style.RESET_ALL)
            return

        dummy_dict = {'title': '', 'country': '', 'date': '', 'content': '', 'link': '', 'wiki_data': ''}
        # Ensure both result lists have the same number of elements
        self.ukraine_pages = self.ukraine_pages + [dummy_dict] * (self.max_results - len(self.ukraine_pages))
        self.russian_pages = self.russian_pages + [dummy_dict] * (self.max_results - len(self.russian_pages))

        # Print formatted results for each row
        for row in range(self.max_results):
            print('-' * self.terminal_width)
            self.print_wrapped_text_with_separator(self.ukraine_pages[row]['title'],
                                                   self.russian_pages[row]['title'])
            self.print_wrapped_text_with_separator(self.ukraine_pages[row]['country'],
                                                   self.russian_pages[row]['country'])
            self.print_wrapped_text_with_separator(self.ukraine_pages[row]['date'],
                                                   self.russian_pages[row]['date'])
            print("\n")
            self.print_wrapped_text_with_separator(self.ukraine_pages[row]['content'], self.russian_pages[row]['content'])
            print("\n")
            self.print_wrapped_text_with_separator(self.ukraine_pages[row]['link'],
                                                   self.russian_pages[row]['link'])

            if self.show_content:
                print('-' * int(self.terminal_width / 2 - 6) + '|DAY EVENTS|' + '-' * int(self.terminal_width / 2 - 6))
                self.print_wrapped_text_with_separator(self.ukraine_pages[row]['wiki_data'],
                                                       self.russian_pages[row]['wiki_data'])
            print('-' * self.terminal_width)

    def print_wrapped_text_with_separator(self, left_text, right_text, separator='|'):
        # Method to print wrapped text with a separator
        # Calculate the width for each section (left, separator, right)
        separator_width = len(separator)
        left_width = (self.terminal_width - separator_width) // 2

        # Wrap the left and right texts
        wrapped_left = textwrap.wrap(left_text, width=left_width)
        wrapped_right = textwrap.wrap(right_text, width=self.terminal_width - left_width - separator_width)

        # Find the maximum number of lines between left and right sections
        max_lines = max(len(wrapped_left), len(wrapped_right))

        # Print the wrapped texts with the separator on each line
        for i in range(max_lines):
            left_line = wrapped_left[i] if i < len(wrapped_left) else ""
            right_line = wrapped_right[i] if i < len(wrapped_right) else ""
            print(f"{left_line.ljust(left_width)} {separator} {right_line}")


# Example usage
if __name__ == "__main__":
    # Create an instance of LuceneSearcher and perform a query
    lucene_searcher = LuceneSearcher()
    lucene_searcher.query_string('Tupolev')
