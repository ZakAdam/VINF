import mwxml
import glob
import re

paths = glob.glob('enwiki*.xml*.bz2')
pattern = re.compile(r'Current events/.*')

def process_dump(dump, path):
  for page in dump:
    if pattern.match(page.title):
    	for revision in page:
            yield page.id, page.title, revision.timestamp, len(revision.text)

for page_id, page_title, rev_timestamp, rev_textlength in mwxml.map(process_dump, paths):
    print("\t".join(str(v) for v in [page_id, page_title, rev_timestamp, rev_textlength]))
