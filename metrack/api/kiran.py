import requests
from bs4 import BeautifulSoup
import re

# URL to scrape
url = "https://www.drishtiias.com/prelims-analysis/2024-prelims-analysis"

# Sending a request to the URL
response = requests.get(url)

# Parsing the content with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Function to check if an element is bold
def is_bold(tag):
    return tag.name in ['b', 'strong'] or (tag.has_attr('style') and 'font-weight' in tag['style'] and 'bold' in tag['style'])

# Finding all bold elements
bold_elements = soup.find_all(is_bold)

# Regex pattern to match lines that start with a number followed by a period
pattern = re.compile(r'^\d+\.')

# Printing bold lines that start with a number followed by a period
for element in bold_elements:
    lines = element.get_text().splitlines()
    for line in lines:
        stripped_line = line.strip()
        if pattern.match(stripped_line):
            print(stripped_line)
