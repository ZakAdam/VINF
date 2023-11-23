import sys
import re
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType

# Start-up command:
# spark-submit --packages com.databricks:spark-xml_2.12:0.17.0
# --executor-memory 512m spark_code.py
# ./spark/enwiki-latest-pages-articles1.xml-p1p41242

# Check for the argument of data file
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_single_dump>")
    sys.exit(1)

# Define REGEX to load only events data from page
events_pattern = r'class=\"current-events-content description\">(.*?)<div class=\"current-events-nav\"'
events_json = {}

# Initialize Spark session
spark = SparkSession.builder.appName("WikipediaSearch").getOrCreate()

# Load Wikipedia dump data with databricks XML library
wiki_df = spark.read.format("com.databricks.spark.xml") \
    .option("rowTag", "page") \
    .load(sys.argv[1])

# Filter only Current Event pages
current_event_df = wiki_df.filter(col("title").like("Portal:Current events/%"))

# Extract title and text
title_text_df = current_event_df.select("title", "revision.text._VALUE")


def format_date(title):
    print(title)
    return title.split('/')[-1].replace(' ', '_')


def format_text(text):
    events_matches = re.search(events_pattern, text, re.DOTALL)
    if events_matches is None:
        return None
    else:
        return events_matches.group(1)


# Create UDFs for the custom functions
custom_title_udf = udf(format_date, StringType())
custom_text_udf = udf(format_text, StringType())

# Apply the UDFs to the title and text columns
modified_title_text_df = title_text_df \
    .withColumn("modified_title", custom_title_udf(col("title"))) \
    .withColumn("modified_text", custom_text_udf(col("_VALUE"))) \
    .select("modified_title", "modified_text")

# Convert DF to RDD then to dict which will be stored as JSON
output_dict = modified_title_text_df.rdd.collectAsMap()

# Save the dictionary as a JSON file
with open("events_json-azak.json", "w") as json_file:
    json.dump(output_dict, json_file, ensure_ascii=False)
