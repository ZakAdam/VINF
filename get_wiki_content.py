from libraries import csv_manager
import requests
import json
import re

df = csv_manager.load_data('data/merged_date_date.csv')
date_counts = df.groupby('wiki_date').size().reset_index(name='count')
events_pattern = r'class=\"current-events-content description\">(.*?)<div class=\"current-events-nav\"'
#events_pattern = r'<b>Armed conflicts and attacks</b>\n</p>(.*?)<p><b>'
events_json = {}
iteration = 0

for date in date_counts['wiki_date']:
    try:
        response = requests.get(f'https://en.wikipedia.org/wiki/Portal:Current_events/{date}')
    except requests.exceptions.RequestException as e:
        print(f"Request encountered an error: {e}")
        continue

    html_content = response.text
    events_matches = re.search(events_pattern, html_content, re.DOTALL)
    if events_matches is None:
        event_data = None
    else:
        event_data = events_matches.group(1)

    events_json[date] = event_data

    iteration += 1
    if iteration % 10 == 0:
        print(iteration)

print("Started writing dictionary to a file")
with open("data/dates_events-all.json", "w") as fp:
    json.dump(events_json, fp)  # encode dict into JSON
print("Done writing dict into .txt file")



