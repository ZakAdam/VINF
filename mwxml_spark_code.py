from pyspark.sql import SparkSession
import mwxml
import json
import re
import sys

# Changed code so it works with spark -> not used
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_single_dump>")
    sys.exit(1)

# Create a Spark session
spark = SparkSession.builder.appName("War Events").getOrCreate()

# Load data name from input
single_dump_path = sys.argv[1]

# Broadcast the pattern variable to all nodes
pattern = re.compile(r'Current events/.*')
pattern_broadcast = spark.sparkContext.broadcast(pattern)

# Read dump with mwxml library
dump = mwxml.Dump.from_file(open(single_dump_path))

# Crete dict which represents results JSON
results = {}

# Go over all pages in dump
for page in dump:
    # If title is Current events page
    if pattern.match(page.title):
        for revision in page:
            # Add to the JSON, wher key is a date and value is text of page
            results[page.title.split('/')[-1].replace(' ', '_')] = revision.text
            print(page.title)

# Save the results to a JSON file
with open("events_json-azak.json", "w") as fp:
    json.dump(results, fp)

print('Script is successfully done :)')

# Stop the Spark session
spark.stop()
