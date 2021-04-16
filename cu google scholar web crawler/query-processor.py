from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch

client = Elasticsearch([{'host': 'localhost', 'port': 9200}])
index_name = 'cu-scholar'
search_handler = Search(using=client, index=index_name)


def search(search_term):
    q = MultiMatch(query=search_term, fields=['title', 'authors'])

    search_response = search_handler.query(q)

    for hit in search_response:
        print(hit.meta.score)
        print(hit.title)
        print(hit.authors)
        print(hit.url)
        print()


search('World malaria report 2015')
