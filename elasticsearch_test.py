from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection

# Connect to Elasticsearch
es = Elasticsearch(["https://localhost:9200"],verify_certs=False,
        connection_class=RequestsHttpConnection,
        port=9200,
        http_auth=('elastic', 'pF85YoMTeAgav4FKI6yu'))

# Create an index
es.indices.create(index='test-index')

# Insert data into the index
es.index(index='test-index', id=1, body={"name": "John Doe", "age": 30})
es.index(index='test-index', id=2, body={"name": "Jane Doe", "age": 25})

# Check if the index exists
if es.indices.exists(index='test-index'):
    print("Index exists.")
else:
    print("Index does not exist.")

# Check the number of documents in the index
count = es.count(index='test-index')
print(f"Number of documents in the index: {count['count']}")

# Perform a search query
res = es.search(index='test-index', body={"query": {"match_all": {}}})

# Print the search results
print(res)
