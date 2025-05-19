import pandas as pd
from bs4 import BeautifulSoup

# Load HTML content from a file or string
with open('bipTableBTC.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')  # or 'html.parser'

# Find all tables (you can also narrow down by class/id/etc.)
tables = soup.find_all('table')

# Convert the first table to DataFrame
dfs = pd.read_html(str(tables[0]))  # pandas reads it from string
df = dfs[0]

# Save to CSV
df.to_csv('bipTableBTC.csv', index=False)
