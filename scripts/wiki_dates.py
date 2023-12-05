# Script to fix missing dates in data
from libraries import csv_manager
import pandas as pd

df = csv_manager.load_data('../data/merged_data.csv')

wiki_values = []
empty_dates_number = 0

# Iterate over all rows in dataframe
for index, row in df.iterrows():
    # Check the number of missing dates -> Around 16
    if pd.isna(row['date']):
        empty_dates_number += 1
        wiki_values.append(None)
        continue

    # Load the date in given format
    parsed_date = pd.to_datetime(row['date'])
    # Then change the format of a date to the wikipedia date format -> YYYY_Month_DD
    wiki_date = f'{str(parsed_date.year)}_{str(parsed_date.strftime("%B"))}_{str(parsed_date.day)}'
    # Add to the array
    wiki_values.append(wiki_date)

# Add new dates as a new column wiki_date
df['wiki_date'] = wiki_values
print('Ended processing...')
print(f'Number of rows without date: {empty_dates_number}')
print('Starting storing data...')

# Store new CSV
csv_manager.store_data('../data/merged_date_date.csv', df)

print('Donzel! :)')
