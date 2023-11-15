import textwrap

import lucene
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.index import DirectoryReader
from java.nio.file import Paths


class LuceneSearcher:
    def __init__(self, index_dir='index', max_results=10):
        lucene.initVM()
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
            pages_dict.append({'link': doc.get("link"), 'country': doc.get("country"), 'date': doc.get("date")})
            '''
            print('----------------------------------------------------------------------------------')
            doc = searcher.doc(hit.doc)
            link = doc.get("link")
            country_result = doc.get("country")
            date = doc.get("date")
            print(f"Link: {link}")
            print(f"Country: {country_result}")
            print(f"Date: {date}")
            print("")
            print('----------------------------------------------------------------------------------')
            '''

        # Close the index reader
        index_reader.close()

    def print_results(self):
        print(self.ukraine_pages)
        print(self.russian_pages)
        for row in range(self.max_results):
            print('----------------------------------------------------------------------------------')
            print(f"{textwrap.fill(self.ukraine_pages[row]['link']).ljust(100)} | {self.russian_pages[row]['link'].rjust(100)}")
            print(f"{self.ukraine_pages[row]['country'].ljust(100)} | {self.russian_pages[row]['country'].rjust(100)}")
            print(f"{self.ukraine_pages[row]['date'].ljust(100)} | {self.russian_pages[row]['date'].rjust(100)}")
            print('----------------------------------------------------------------------------------')


# Example usage
if __name__ == "__main__":
    lucene_searcher = LuceneSearcher()
    lucene_searcher.query_string('Tupolev')



'''
import lucene
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.index import DirectoryReader
from java.nio.file import Paths


class LuceneSearcher:
    def __init__(self, index_dir='index', max_results=10):
        lucene.initVM()
        self.index_dir = index_dir
        self.max_results = max_results
        self.index = MMapDirectory(Paths.get(index_dir))
        self.searcher = IndexSearcher(DirectoryReader.open(self.index))
        self.analyzer = StandardAnalyzer()

    def query_string(self, string='Russia', max_results=10):
        query_parser = QueryParser("content", self.analyzer)
        index_reader = DirectoryReader.open(self.index)
        searcher = IndexSearcher(index_reader)

        query = query_parser.parse(string)
        hits = searcher.search(query, max_results)

        # Iterate through the search results
        for hit in hits.scoreDocs:
            print('----------------------------------------------------------------------------------')
            doc = searcher.doc(hit.doc)
            link = doc.get("link")
            country = doc.get("country")
            date = doc.get("date")
            #content = doc.get("content")
            print(f"Link: {link}")
            print(f"Country: {country}")
            print(f"Date: {date}")
            #print(f"Content: {content}")
            print("")
            print('----------------------------------------------------------------------------------')

        # Close the index reader
        index_reader.close()


# Example usage
if __name__ == "__main__":
    lucene_searcher = LuceneSearcher()
    lucene_searcher.query_string('Tupolev')
'''