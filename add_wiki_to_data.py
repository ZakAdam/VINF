from libraries import csv_manager
import pandas as pd
import json

df = csv_manager.load_data('data/merged_date_date.csv')

with open("data/dates_events-all.json", "r") as fp:
    # Load the dictionary from the file
    events_dict = json.load(fp)

wiki_data = []
empty_dates_number = 0

#for index, row in df.iterrows():
for index, row in df.iterrows():
    if pd.isna(row['wiki_date']):
        empty_dates_number += 1
        wiki_data.append(None)
        continue

    events_data = events_dict[row['wiki_date']]
    wiki_data.append(events_data)


df['wiki_data'] = wiki_data
print('Ended processing...')
print(f'Number of rows without date: {empty_dates_number}')
print('Starting storing data...')

csv_manager.store_data('data/data_all.csv', df)

print('Donzel! :)')
