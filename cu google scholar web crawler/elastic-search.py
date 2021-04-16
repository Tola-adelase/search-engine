import json
import requests
from elasticsearch import Elasticsearch

# res = requests.get('http://localhost:9200')
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


res = es.search(index="cu-scholar", body={
    'query': {
        'match': {
            'name': 'Mason'
        }
    }
}
                )
print(json.dumps(res, indent=2))
