# Importing all the needed libraries
import json
import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from urllib.parse import parse_qs, urlparse

# Elastic search
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.181 Safari/537.36',
    'Pragma': 'no-cache'
}
index_name = 'cu-scholar'


def next_page_link(page_content):
    try:
        _link = page_content.find('button', {'aria-label': 'Next'}).get('onclick')
    except:
        print(page_content)
    _link = str(_link.split("'")[1]).replace('\\x3d', '=').replace('\\x26', '&')
    _link = 'https://scholar.google.co.uk' + _link

    return _link


def process_profiles(page_content):
    profiles = []

    # Scrapped paginated profile link of the staff.
    profile_links = page_content.findAll('a', {'class': 'gs_ai_pho'})

    # Pushing the data into datastore
    for index in range(0, len(profile_links)):
        profile_link = 'https://scholar.google.co.uk' + profile_links[index].get('href')

        profiles.append(process_articles(profile_link))

    return profiles


def index_article(article):
    # Elastic search Indexing
    doc_id = article.get('id')
    es.index(index=index_name, id=doc_id, body=article)


def fetch_article_data(article_link):
    response = requests.get(article_link, headers=headers)
    content = BeautifulSoup(response.text, 'lxml')

    table = content.find('div', {'id': 'gsc_vcd_table'})
    rows = table.find_all('div', {'class': 'gs_scl'})

    authors = list(filter(lambda row: row.find('div', {'class': 'gsc_vcd_field'}).string == 'Authors', rows))

    try:
        authors = authors[0].find('div', {'class': 'gsc_vcd_value'}).string.split(', ')
    except:
        authors = ''

    author_id = content.find('input', {'id': 'gsc_vcd_cid'}).get('value')

    return {
        'authors': authors,
        'id': author_id
    }


def process_articles(profile_link):
    response = requests.get(profile_link, headers=headers)
    content = BeautifulSoup(response.text, 'lxml')

    # Scrapping list of articles/papers
    table = content.find('table', {'id': 'gsc_a_t'})
    table_body = table.find('tbody', {'id': 'gsc_a_b'})

    rows = table_body.findAll('tr', {'class': 'gsc_a_tr'})

    for row in rows:
        cols = row.find('td', {'class': 'gsc_a_t'})
        article_data = cols.find('a', {'class': 'gsc_a_at'})
        article_url = 'https://scholar.google.co.uk' + article_data.get('data-href')
        add_article_data = fetch_article_data(article_url)
        # Scrapping data from papers/articles
        if '' != add_article_data.get('authors'):
            article = {
                'id': add_article_data.get('id'),
                'authors': add_article_data.get('authors'),
                'title': article_data.string,
                'url': article_url
            }
            index_article(article)


def myCrawler(initial_url, num_pages):
    current_page = 1
    current_page_url = initial_url

    while current_page <= num_pages:
        response = requests.get(current_page_url, headers=headers)
        content = BeautifulSoup(response.text, 'lxml')

        # Process content
        process_profiles(content)

        # Update current page URL
        current_page_url = next_page_link(content)

        # Increment current page after processing
        current_page += 1
    last_page_url = current_page_url
    print(last_page_url)


myCrawler('https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779', 5)
