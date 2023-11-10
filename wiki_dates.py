import requests
import re
from libraries import csv_manager
import pandas as pd

df = csv_manager.load_data('data/merged_data.csv')

wiki_values = []
empty_dates_number = 0

#for index, row in df.iterrows():
for index, row in df.iterrows():
    if pd.isna(row['date']):
        empty_dates_number += 1
        wiki_values.append(None)
        continue

    #print(row['date'])
    parsed_date = pd.to_datetime(row['date'])
    #print(parsed_date)
    wiki_date = f'{str(parsed_date.year)}_{str(parsed_date.strftime("%B"))}_{str(parsed_date.day)}'
    #print(wiki_date)
    # df.at[index, 'wiki_date'] = wiki_date
    wiki_values.append(wiki_date)

    #if index > 5: break

df['wiki_date'] = wiki_values
print('Ended processing...')
print(f'Number of rows without date: {empty_dates_number}')
print('Starting storing data...')

#csv_manager.store_data('data/merged_date_date.csv', df[0:5])
csv_manager.store_data('data/merged_date_date.csv', df)

print('Donzel! :)')
