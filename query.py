import lucene
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.index import DirectoryReader
from java.nio.file import Paths
from java.io import File

# Initialize PyLucene
lucene.initVM()

# Specify the directory where the MMap index is stored
index_dir = 'index'  # Adjust to your index directory

# Open the MMap index
index = MMapDirectory(Paths.get(index_dir))
index_reader = DirectoryReader.open(index)
searcher = IndexSearcher(index_reader)

# Create a query parser and specify the field to search in (e.g., "content")
analyzer = StandardAnalyzer()


def query_string(string='Russia'):
    query_parser = QueryParser("content", analyzer)
    index_reader = DirectoryReader.open(index)
    searcher = IndexSearcher(index_reader)

    query = query_parser.parse(string)
    hits = searcher.search(query, 100)  # Limit the number of results to retrieve (adjust as needed)
    #print(f'Number of hits: {len(hits)}')

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


#query_string('Nothing to worry about,')
query_string('Tupolev')
