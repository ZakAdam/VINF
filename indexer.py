import lucene
import csv
import sys

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

print('LUCENE is running')
csv.field_size_limit(sys.maxsize)

file = 'data/data_all.csv'
index_dir = 'index'
# Create the index
analyzer = StandardAnalyzer()
config = IndexWriterConfig(analyzer)
index = MMapDirectory(Paths.get(index_dir))  # Use MMapDirectory for file-based storage
writer = IndexWriter(index, config)

count = 0
with open(file, 'r') as file:
    csv_reader = csv.reader(file, delimiter='\t')

    # Skip the header line if needed
    next(csv_reader, None)

    for row in csv_reader:
        doc = Document()
        doc.add(Field('title', row[1], TextField.TYPE_STORED))
        doc.add(Field('link', row[2], TextField.TYPE_STORED))
        doc.add(Field('country', row[3], TextField.TYPE_STORED))
        doc.add(Field('date', row[4], TextField.TYPE_STORED))
        doc.add(Field('content', row[5], TextField.TYPE_STORED))
        doc.add(Field('Wiki Events', row[7], TextField.TYPE_STORED))
        writer.addDocument(doc)

        count += 1
        if count % 1000 == 0:
            print(f'{count} records saved!')

    file.close()

# Commit and close the writer
writer.commit()
writer.close()
print(f'Number of lines processed: {count}')
