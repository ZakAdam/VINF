import textwrap
import shutil

import lucene
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.index import DirectoryReader
from java.nio.file import Paths


class LuceneSearcher:
    def __init__(self, index_dir='index', max_results=10):
        #lucene.initVM()
        self.index_dir = index_dir
        self.max_results = max_results
        self.index = MMapDirectory(Paths.get(index_dir))
        self.searcher = IndexSearcher(DirectoryReader.open(self.index))
        self.analyzer = StandardAnalyzer()
        self.ukraine_pages = []
        self.russian_pages = []

    def query_string(self, query_str='Russia'):
        self.search_by_country(query_str, 'Ukraine', self.ukraine_pages)
        self.search_by_country(query_str, 'Russia', self.russian_pages)
        self.print_results()

    def search_by_country(self, query_str, country, pages_dict):
        query_parser = QueryParser("content", self.analyzer)
        index_reader = DirectoryReader.open(self.index)
        searcher = IndexSearcher(index_reader)

        # Construct a query with both the input string and the country filter
        query_string = f'({query_str}) AND country:{country}'
        query = query_parser.parse(query_string)
        hits = searcher.search(query, self.max_results)

        # Print the search results
        print(f"Results for '{query_str}' in {country}:\n")
        for hit in hits.scoreDocs:
            doc = searcher.doc(hit.doc)
            pages_dict.append({'link': doc.get("link"),
                               'title': doc.get("title"),
                               'country': doc.get("country"),
                               'content': doc.get('content'),
                               'date': doc.get("date")})

        # Close the index reader
        index_reader.close()

    def print_results(self):

        line_width = 80

        for row in range(self.max_results):
            print('----------------------------------------------------------------------------------')
            print(f"{textwrap.fill(self.ukraine_pages[row]['title']).ljust(100)} | {self.russian_pages[row]['title'].rjust(100)}")
            print(f"{self.ukraine_pages[row]['country'].ljust(100)} | {self.russian_pages[row]['country'].rjust(100)}")
            print(f"{self.ukraine_pages[row]['date'].ljust(100)} | {self.russian_pages[row]['date'].rjust(100)}")
            print("\n")
            self.print_wrapped_text_with_separator(self.ukraine_pages[row]['content'], self.russian_pages[row]['content'])
            print("\n")
            print(f"{textwrap.fill(self.ukraine_pages[row]['link']).ljust(100)} | {self.russian_pages[row]['link'].rjust(100)}")
            print('----------------------------------------------------------------------------------')

    def print_wrapped_text_with_separator(self, left_text, right_text, separator='|'):
        # Get the terminal width
        terminal_width, _ = shutil.get_terminal_size()

        # Calculate the width for each section (left, separator, right)
        separator_width = len(separator)
        left_width = (terminal_width - separator_width) // 2

        # Wrap the left and right texts
        wrapped_left = textwrap.wrap(left_text, width=left_width)
        wrapped_right = textwrap.wrap(right_text, width=terminal_width - left_width - separator_width)

        # Find the maximum number of lines between left and right sections
        max_lines = max(len(wrapped_left), len(wrapped_right))

        # Print the wrapped texts with the separator on each line
        for i in range(max_lines):
            left_line = wrapped_left[i] if i < len(wrapped_left) else ""
            right_line = wrapped_right[i] if i < len(wrapped_right) else ""
            print(f"{left_line.ljust(left_width)} {separator} {right_line}")


# Example usage
if __name__ == "__main__":
    lucene_searcher = LuceneSearcher()
    lucene_searcher.query_string('Tupolev')
