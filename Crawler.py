import code
import os
from pickle import GET

import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import json
import webbrowser
import feedparser

# webbrowser.open(url)

for page_num in range(1, 10):
    # get next page url
    url = url + str(page_num)


def crawler(seed, maxcount):
    global url
    Q = [seed]  # this is the queue which initially contains the given seed URL
    count = 0
    while Q != [] and count < maxcount:
        count += 1
        url = Q[0]
        Q = Q[1:]
        print(":" + url)

        # def fetch(url):
        # try:
    # except requests.exceptions.ConnectionError:
    # print('Given URL: "%s" is not available!' % url)
    # return

    mode = requests.get(url)
    plain = mode.text
    s = BeautifulSoup(plain, "html.parser")

    for link in s.findAll('a', {'class': 'gs_ai_pho'}):

        new_url = link.get('href')
        if new_url is not None and new_url != '/':
            new_url = new_url.strip()
            # print("new_url is : ", new_url)

            # normalise if needed
            if new_url[0:7] != 'https://' and new_url[0:8] != 'https://':
                if url[len(url):0] == '/':
                    new_url = 'https:' + url.strip(
                        '/citations?view_op=view_org&hl=en&org=9117984065169182779') + new_url
                else:
                    new_url = 'https' + url.strip(
                        '/citations?view_op=view_org&hl=en&org=9117984065169182779') + new_url
                    Q.append(new_url)

                    # loop over links
                    for ink in link:
                        # try to crawl links recursively
                        try:
                            # use only links starting with 'http'
                            if 'http' in link['href']:
                                crawler(link['href'], - 1)
                        # ignore internal links
                        except KeyError:
                            pass
                    print(len(new_url))
                    print("new_url is : ", new_url)  # uncomment the print statement to see the urls


crawler('https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779', 10)
