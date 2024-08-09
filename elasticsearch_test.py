import os
from elasticsearch import Elasticsearch, exceptions
from elasticsearch import RequestsHttpConnection

def connect_to_elasticsearch():
    """Establishes connection to the Elasticsearch instance."""
    es_host = os.getenv('ES_HOST', 'http://localhost:9200')
    es_port = os.getenv('ES_PORT', '9200')
    es_username = os.getenv('ES_USERNAME', 'elastic')
    es_password = os.getenv('ES_PASSWORD', '')

    return Elasticsearch(
        [es_host],
        verify_certs=False,
        connection_class=RequestsHttpConnection,
        port=es_port,
        http_auth=(es_username, es_password)
    )

def create_index(es, index_name):
    """Creates an index if it doesn't already exist."""
    if not es.indices.exists(index=index_name):
        try:
            es.indices.create(index=index_name)
            print(f"Index '{index_name}' created successfully.")
        except exceptions.RequestError as e:
            print(f"Error creating index '{index_name}': {e.info}")
    else:
        print(f"Index '{index_name}' already exists.")

def insert_data(es, index_name):
    """Inserts sample data into the specified index."""
    es.index(index=index_name, id=1, body={"name": "John Doe", "age": 30})
    es.index(index=index_name, id=2, body={"name": "Jane Doe", "age": 25})

def count_documents(es, index_name):
    """Returns the number of documents in the specified index."""
    count = es.count(index=index_name)
    return count['count']

def search_documents(es, index_name):
    """Performs a search query and returns the results."""
    return es.search(index=index_name, body={"query": {"match_all": {}}})

def main():
    es = connect_to_elasticsearch()
    index_name = 'test-index'
    
    try:
        create_index(es, index_name)
        insert_data(es, index_name)
        
        num_documents = count_documents(es, index_name)
        print(f"Number of documents in the index '{index_name}': {num_documents}")
        
        search_results = search_documents(es, index_name)
        print("Search results:")
        for hit in search_results['hits']['hits']:
            print(hit['_source'])
    
    except exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
