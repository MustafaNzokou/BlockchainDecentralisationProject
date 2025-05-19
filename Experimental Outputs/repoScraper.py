import requests
from bs4 import BeautifulSoup
import json

url = 'https://github.com/bitcoin/bips'
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')

soup = BeautifulSoup(html_content, 'html.parser')

repo_name = soup.find('strong', {'itemprop': 'name'}).text.strip()
repo_description = soup.find('p', {'class': 'f4 mb-3'}).text.strip()

readme_url = f'https://raw.githubusercontent.com/{repo_name}/master/README.md'
readme_response = requests.get(readme_url)

if readme_response.status_code == 200:
    readme_content = readme_response.text
else:
    readme_content = None

repo_data = {
    'name': repo_name,
    'description': repo_description,
    'readme': readme_content
}

with open('repo_data.json', 'w') as json_file:
    json.dump(repo_data, json_file, indent=4)