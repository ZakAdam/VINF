# Script to merge data loaded from multiple sites to one big CSV file
from libraries import csv_manager
import pandas as pd

# Load all data files
independent = csv_manager.load_data('../data/data-tags.csv')
post = csv_manager.load_data('../data/data-post.csv')
times = csv_manager.load_data('../data/data-moscow.csv')
tass = csv_manager.load_data('../data/data-tass.csv')

# Combine them to one dataframe
merged_df = pd.concat([independent, post, times, tass])

# Store new dataframe
csv_manager.store_data('../data/merged_data.csv', merged_df)
print('Done!')
