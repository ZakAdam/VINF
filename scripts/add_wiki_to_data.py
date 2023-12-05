from libraries import csv_manager
import pandas as pd
import json

df = csv_manager.load_data('../data/merged_date_date.csv')

with open("../data/dates_events-all.json", "r") as fp:
    # Load the dictionary from the file
    events_dict = json.load(fp)

wiki_data = []
empty_dates_number = 0

for index, row in df.iterrows():
    # Check if wiki_date is empty
    if pd.isna(row['wiki_date']):
        empty_dates_number += 1
        wiki_data.append(None)
        continue

    # Get events from JSON where key is a date loaded from CSV data
    events_data = events_dict[row['wiki_date']]
    # Add events to the resulting array
    wiki_data.append(events_data)

# Add array as new column to the dataframe
df['wiki_data'] = wiki_data
print('Ended processing...')
print(f'Number of rows without date: {empty_dates_number}')
print('Starting storing data...')

# Store new dataframe as new CSV data
csv_manager.store_data('../data/data_all.csv', df)

print('Donzel! :)')
