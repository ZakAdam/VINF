import requests
import re

#for i in range(1, 32):
#    print(f'https://en.wikipedia.org/wiki/Portal:Current_events/2022_October_{i}')

response = requests.get('https://www.kyivpost.com/post/10000')
html_content = response.text
#date_pattern = r'<div class=\"post-info\">.+?</a>(.*?)</div>'
date_pattern = r'<div class=\"post-info\">.+?</a>.*?(\w+ \d{1,2}, \d{4},\s+\d{1,2}:\d{2} [ap]m).*?</div>'
# date_pattern = r'<div class=\"post-info\">(\w+ \d{1,2}, \d{4}, \s\d{1,2}:\d{2} [ap]m)</div>'

pattern = r"(\w+ \d{1,2}, \d{4},\s+\d{1,2}:\d{2} [ap]m)"

match = re.search(pattern, html_content, re.DOTALL)

if match:
    date = match.group(1)
    print(date)

# Find the date within the container
match = re.search(date_pattern, html_content, re.DOTALL)

date = match.group(1)
print(date)

article_pattern = r'(<div id=\"post-content\">)(.*)\n</section>'
article_matches = re.search(article_pattern, html_content, re.DOTALL)

script_pattern = r'<script.*?</script>'
div_pattern = r'<div.*?</div>'
#div_pattern = r'<div.*?<p'
# Remove script elements and their contents
cleaned_html = re.sub(script_pattern, '', article_matches.group(2).replace('\t', ' '), flags=re.DOTALL)
cleaned_html2 = re.sub(div_pattern, '', cleaned_html, flags=re.DOTALL)

print(cleaned_html2)

