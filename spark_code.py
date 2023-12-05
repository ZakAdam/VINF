# Spark script used to parse Wikipedia data on cluster -> this got used
import sys
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType, StructType, StructField

# Start-up command:
# spark-submit --packages com.databricks:spark-xml_2.12:0.17.0
# --executor-memory 512m spark_code.py
# ./spark/enwiki-latest-pages-articles1.xml-p1p41242

# Check for the argument of data file
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_single_dump>")
    sys.exit(1)

# Define REGEX to load only events data from page
events_pattern = r"<!-- All news items below this line -->.'(.*?)<!-- All news items above this line -->"

# Initialize Spark session
spark = SparkSession.builder.appName("WikipediaSearch").getOrCreate()

# Define the custom schema for the DataFrame
custom_schema = StructType([
    StructField("title", StringType(), True),
    StructField("revision", StructType([
        StructField("text", StructType([
            StructField("_VALUE", StringType(), True)
        ]), True)
    ]), True)
])

# Load Wikipedia dump data with databricks XML library
wiki_df = spark.read.format("com.databricks.spark.xml") \
    .option("rowTag", "page") \
    .schema(custom_schema) \
    .load(sys.argv[1])

# Filter only Current Event pages
current_event_df = wiki_df.filter(col("title").like("Portal:Current events/%"))


# Custom method used to get date from title of the page.
# It cannot be loaded from revision date as it is a date of last change not event date.
def format_date(title):
    return title.split('/')[-1].replace(' ', '_')


# Custom method used to get only important content from wikipedia page
def format_text(text):
    if text is None:
        return None

    events_matches = re.search(events_pattern, text, re.DOTALL)

    # If no content is found, return None
    if events_matches is None:
        return None
    else:
        return events_matches.group(1)


# Create UDFs for the custom functions
custom_title_udf = udf(format_date, StringType())
custom_text_udf = udf(format_text, StringType())

# Apply the UDFs to the title and text columns
modified_title_text_df = current_event_df \
    .withColumn("modified_title", custom_title_udf(col("title"))) \
    .withColumn("modified_text", custom_text_udf(col("revision.text._VALUE"))) \
    .select("modified_title", "modified_text")

# Write the data to the JSONs in directory
modified_title_text_df.write.json('events_json-azak', mode='overwrite')
