import json
import re

import requests
from bs4 import BeautifulSoup
import csv
import time

headers = {
    'User-Agent': 'Adetola Adelase',
    'From': 'adelasea@uni.coventry.ac.uk'
}

f = csv.writer(open('No.csv', 'w'))
f.writerow(['Name', 'Profile'])

start_url = 'https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779'
response = requests.get(start_url, headers=headers)
content = BeautifulSoup(response.text, 'lxml')

page_count_links = content.findAll('button',
                                   {'type': 'button'})
num_pages = str(page_count_links[1]).split(" ")[8].split("=")[2]
print(str(page_count_links[1]).split(" ")[8].split("=")[2])
try:  # Make sure there are more than one page, otherwise, set to 1.
    num_pages = str(page_count_links[1]).split(" ")[8].split("=")[2]
except IndexError:
    num_pages = 1

url_list = ["{}+{}".format(start_url, num_pages)]
new_url = 'https://scholar.google.co.uk' + num_pages.replace("'", "")
final_url = new_url.replace("\\","/")
print(final_url)

name = content.findAll('h3', {'class': 'gs_ai_name'})
links = content.findAll('a', {'class': 'gs_ai_pho'})
dept = content.findAll('div', {'class': 'gs_ai_aff'})
title = content.findAll('div', {'class': 'gs_ai_int'})
papers = content.findAll('a', {'class': 'gsc_a_at'})
names_on_papers = content.findAll('div', {'class': 'gs_gray'})

print(len(links), len(name))

for index in range(0, len(links)):
    page = {
        'name': name[index].text.strip().replace('\n', ''),
        'url': 'https://scholar.google.co.uk' + links[index]['href'],
        'dept': dept[index].text.strip().replace('\n', ''),
        'title': title[index].text.replace(' ', ', '),
        # 'papers': start_url + papers[index]['data-href'].strip().replace('\n', ''),
        # 'names_on_papers': names_on_papers[index].text.strip().replace('\n', ''),

    }

    print(json.dumps(page, indent=4))

for index in range(0, len(name)):
    names = name[index].text.strip().replace('\n', '')
    profile = 'https://scholar.google.co.uk' + links[index]['href']

    # f.writerow([names, profile])
