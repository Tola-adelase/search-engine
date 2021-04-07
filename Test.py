# Libraries
import json
import requests
from bs4 import BeautifulSoup

start_url = 'https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779'

for page_num in range(1, 10):
    url = start_url + str(page_num)

    response = requests.get(url)
    content = BeautifulSoup(response.text, 'lxml')

    links = content.findAll('h3', {'class': 'gs_ai_name'})
    name = content.findAll('div', {'class': 'gs_ai_aff'})
    title = content.findAll('div', {'class': 'gs_ai_int'})

    print('\n\nURL:', url)

    for index in range(0, len(links)):
        page = {
            'name': name[index].text,
            'url': links[index]['href'],
            'title': title[index].text.strip().replace('\n', ''),

        }

        print(json.dumps(page, indent=2))
