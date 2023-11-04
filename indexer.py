import lucene
import csv

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import MMapDirectory
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher
from java.io import File
from java.nio.file import Paths

lucene.initVM()

print('LUCENE is running?')

index_dir = 'moscow_index'
# Create the index
analyzer = StandardAnalyzer()
config = IndexWriterConfig(analyzer)
index = MMapDirectory(Paths.get(index_dir))  # Use MMapDirectory for file-based storage
writer = IndexWriter(index, config)

count = 0
with open('data/data-moscow.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter='\t')

    # Skip the header line if needed
    next(csv_reader, None)

    for row in csv_reader:
        print(f"Column 1: {row[0]}, Column 2: {row[1]}")

        doc = Document()
        doc.add(Field('title', row[1], TextField.TYPE_STORED))
        doc.add(Field('link', row[2], TextField.TYPE_STORED))
        doc.add(Field('country', row[3], TextField.TYPE_STORED))
        doc.add(Field('date', row[4], TextField.TYPE_STORED))
        doc.add(Field('content', row[5], TextField.TYPE_STORED))
        writer.addDocument(doc)

        count += 1
        if count > 10: break

    file.close()

# Commit and close the writer
writer.commit()
writer.close()
print(f'Number of lines: {count}')


def query_string(string='Russia'):
    query_parser = QueryParser("content", analyzer)
    index_reader = DirectoryReader.open(index)
    searcher = IndexSearcher(index_reader)

    query = query_parser.parse(string)
    hits = searcher.search(query, 10)  # Limit the number of results to retrieve (adjust as needed)
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


query_string('missile')
