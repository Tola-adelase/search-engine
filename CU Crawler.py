import requests
from bs4 import BeautifulSoup
import json
import csv

headers = {
    'User-Agent': 'Adetola Adelase',
    'From': 'adelasea@uni.coventry.ac.uk'
}

f = csv.writer(open('Information Retrieval.csv', 'w'))
f.writerow(['Name', 'Profile'])


current_page_url = 'https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779'
current_page = 1
num_pages = 3


def next_page_link(page_content):
    pagination_links = page_content.findAll('button', {'type': 'button'})
    next_page = str(pagination_links[1]).split(" ")[8].split("=")[2].replace("'", "").replace('"', "")
    next_page = 'https://scholar.google.co.uk/' + next_page.replace('\\x3d', '=').replace('\\x26', '&')

    return next_page


def process_profiles(page_content):
    # Extract data from page
    name = content.findAll('h3', {'class': 'gs_ai_name'})
    profile_link = content.findAll('a', {'class': 'gs_ai_pho'})
    dept = content.findAll('div', {'class': 'gs_ai_aff'})
    topics = content.findAll('div', {'class': 'gs_ai_int'})
    # articles = process_articles(profile_link)

    # Push data into datastore
    for index in range(0, len(profile_link)):
        page = {
            'name': name[index].text.strip().replace('\n', ''),
            'url': 'https://scholar.google.co.uk' + profile_link[index]['href'],
            'dept': dept[index].text.strip().replace('\n', ''),
            'topics': topics[index].text.replace(' ', ', ').replace(',', '.'),
        }
        print(json.dumps(page, indent=4))

    return


def process_articles(profile_link):
    # response = requests.get(profile_link, headers=headers)
    # content = BeautifulSoup(response.text, 'lxml')

    # Index articles listed on page

    # Add indexed articles to array
    articles = []

    return articles


while current_page <= num_pages:
    response = requests.get(current_page_url, headers=headers)
    content = BeautifulSoup(response.text, 'lxml')

    # Process content
    process_profiles(content)

    # Update current page URL
    current_page_url = next_page_link(content)

    # Increment current page after processing
    current_page += 1
