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


# Define a class for Lucene indexing functionality
class LuceneIndexer:
    # Load all Lucene required objects and index directory + data file
    def __init__(self, index_dir='index', csv_file='data/data_all.csv'):
        # Initialize LuceneIndexer with default parameters
        csv.field_size_limit(sys.maxsize)
        self.csv_file = csv_file
        self.index_dir = index_dir
        self.analyzer = StandardAnalyzer()  # Lucene standard text analyzer
        self.config = IndexWriterConfig(self.analyzer)
        self.index = MMapDirectory(Paths.get(index_dir))  # Lucene index directory
        self.writer = IndexWriter(self.index, self.config)

    def index_csv(self):
        count = 0
        # Open and read data file
        with open(self.csv_file, 'r') as file:
            csv_reader = csv.reader(file, delimiter='\t')

            # Skip the header line if needed
            next(csv_reader, None)

            # Process and store each row to the index
            for row in csv_reader:
                doc = Document()
                # Add fields to the Lucene document
                doc.add(Field('title', row[1], TextField.TYPE_STORED))
                doc.add(Field('link', row[2], TextField.TYPE_STORED))
                doc.add(Field('country', row[3], TextField.TYPE_STORED))
                doc.add(Field('date', row[6], TextField.TYPE_STORED))
                doc.add(Field('content', row[5], TextField.TYPE_STORED))
                doc.add(Field('Wiki Events', row[7], TextField.TYPE_STORED))
                self.writer.addDocument(doc)

                count += 1
                if count % 1000 == 0:
                    print(f'{count} records saved!')

            file.close()

        # Commit and close the writer
        self.writer.commit()
        self.writer.close()
        print(f'Number of lines processed: {count}')


# Example usage
if __name__ == "__main__":
    # Create an instance of LuceneIndexer and perform CSV indexing
    lucene_indexer = LuceneIndexer()
    lucene_indexer.index_csv()
