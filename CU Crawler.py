import json
import requests
from bs4 import BeautifulSoup

start_url = 'https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779'


def fetch(url):
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Given URL: "%s" is not available!' % url)
        return

    content = BeautifulSoup(response.text, 'lxml')

    links = content.findAll('a', {'class': 'gs_ai_pho'})
    name = content.findAll('h3', {'class': 'gs_ai_name'})
    dept = content.findAll('div', {'class': 'gs_ai_aff'})
    cited = content.findAll('div', {'class': 'gs_ai_cby'})
    title = content.findAll('div', {'class': 'gs_ai_int'})

    print(len(links), len(name))
    for index in range(0, len(name)):
        page = {
            'name': name[index].text.strip().replace('\n', ''),
            'dept': dept[index].text.strip().replace('\n', ''),
            'title': title[index].text,
            'cited': cited[index].text.strip().replace('\n', ''),
            'url': links[index]['href'],

        }
        print(json.dumps(page, indent=2))


fetch(start_url)
