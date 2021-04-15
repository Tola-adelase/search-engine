# Importing all the needed libraries
import json
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Adetola Adelase',
    'From': 'adelasea@uni.coventry.ac.uk'
}


def next_page_link(page_content):
    _link = page_content.find('button', {'aria-label': 'Next'}).get('onclick')
    _link = str(_link.split("'")[1]).replace('\\x3d', '=').replace('\\x26', '&')
    _link = 'https://scholar.google.co.uk/' + _link

    return _link


def process_profiles(page_content):
    # Extract data from page
    names = page_content.findAll('h3', {'class': 'gs_ai_name'})
    profile_links = page_content.findAll('a', {'class': 'gs_ai_pho'})
    depts = page_content.findAll('div', {'class': 'gs_ai_aff'})
    topics = page_content.findAll('div', {'class': 'gs_ai_int'})

    profiles = []

    # Push data into datastore
    for index in range(0, len(names)):
        profile_link = 'https://scholar.google.co.uk' + profile_links[index].get('href')
        user_topics = topics[index].find_all('a')
        user_topics = list(map(lambda topic: topic.string, user_topics))
        page = {
            'name': names[index].string,
            'url': profile_link,
            'dept': depts[index].string,
            'topics': user_topics,
            # 'articles': process_articles(profile_link)
        }
        profiles.append(page)

    return profiles


def process_articles(profile_link):
    response = requests.get(profile_link, headers=headers)
    content = BeautifulSoup(response.text, 'lxml')

    # Index articles listed on page
    articles_data = []
    table = content.find('table', {'id': 'gsc_a_t'})
    table_body = table.find('tbody', {'id': 'gsc_a_b'})

    rows = table_body.findAll('tr', {'class': 'gsc_a_tr'})

    for row in rows:
        cols = row.find('td', {'class': 'gsc_a_t'})
        article = cols.find('a', {'class': 'gsc_a_at'})

        articles_data.append({
            'title': article.string,
            'url': 'https://scholar.google.co.uk' + article.get('data-href')
        })

    return articles_data


def myCrawler(initial_url, num_pages):
    current_page = 1
    current_page_url = initial_url
    pages = {}
    while current_page <= num_pages:
        response = requests.get(current_page_url, headers=headers)
        content = BeautifulSoup(response.text, 'lxml')

        # Process content
        profiles = process_profiles(content)
        pages['page ' + str(current_page)] = profiles

        # Update current page URL
        current_page_url = next_page_link(content)

        # Increment current page after processing
        current_page += 1
    last_page_url = current_page_url
    print(json.dumps(pages, indent=4))


myCrawler('https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779', 5)
