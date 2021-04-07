# Libraries
import json
import requests
from bs4 import BeautifulSoup

start_url = 'https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779'

for page_num in range(1, 10):
    url = start_url + str(page_num)

    response = requests.get(url)
    content = BeautifulSoup(response.text, 'lxml')

    links = content.findAll('a', {'class': 'gs_ai_pho'})
    name = content.findAll('h3', {'class': 'gs_ai_name'})
    title = content.findAll('div', {'class': 'gs_ai_aff'})

    print('\n\nURL:', url)

    for index in range(0, len(name)):
        page = {
            'title': name[index].text,
            'url': links[index]['href'],
            'name': name[index].text.strip().replace('\n', ''),

        }

        print(json.dumps(page, indent=2))
