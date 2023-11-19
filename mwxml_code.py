import mwxml
import json
import glob
import re

# I don't know the correct path to the data file, so it will be fixed later :)
paths = glob.glob('spark/enwiki*.xml*.bz2')
pattern = re.compile(r'Current events/.*')
events_json = {}


def process_dump(dump, path):
    for page in dump:
        if pattern.match(page.title):
            for revision in page:
                yield page.id, page.title, page.title.split('/')[-1].replace(' ', '_'), revision.text


for page_id, page_title, title_date, text in mwxml.map(process_dump, paths):
    events_json[title_date] = text
    print("\t".join(str(v) for v in [page_id, page_title, title_date]))

with open("events_json-azak.json", "w") as fp:
    json.dump(events_json, fp)

print('Script is successfully done :)')
