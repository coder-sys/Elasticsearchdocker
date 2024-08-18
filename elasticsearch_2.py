from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch import RequestsHttpConnection

def main():
    # Connect to Elasticsearch
    es = Elasticsearch(["https://localhost:9200"],verify_certs=False,
        connection_class=RequestsHttpConnection,
        port=9200,
        http_auth=('elastic', '2dfXbwB-BwKnijAbfR0p'))
    # Define index name and settings
    index_name = 'my_index'
    settings = {
        "settings": {
            "index": {
                "refresh_interval": "1s"  # Adjust as needed for real-time performance
            }
        },
        "mappings": {
            "properties": {
                "field1": { "type": "text" },
                "field2": { "type": "keyword" }
            }
        }
    }

    # Create the index if it doesn't exist
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=settings)
        print(f"Index '{index_name}' created.")

    # Index documents
    doc1 = {"field1": "value1", "field2": "value2"}
    es.index(index=index_name, id=1, body=doc1)
    print("Document 1 indexed.")

    # Bulk index documents
    actions = [
        {"_index": index_name, "_id": 2, "_source": {"field1": "value3", "field2": "value4"}},
        {"_index": index_name, "_id": 3, "_source": {"field1": "value5", "field2": "value6"}}
    ]
    bulk(es, actions)
    print("Bulk documents indexed.")

    # Refresh the index
    es.indices.refresh(index=index_name)
    print("Index refreshed.")

    # Perform a search query
    query = {
        "query": {
            "match": {
                "field1": "value1"
            }
        }
    }
    response = es.search(index=index_name, body=query, refresh=True)
    print("Search results:", response)

if __name__ == "__main__":
    main()
