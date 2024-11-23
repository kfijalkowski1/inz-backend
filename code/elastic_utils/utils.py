from elasticsearch import Elasticsearch

es_client = Elasticsearch("https://localhost:9200/", basic_auth=("elastic", "lBHjhTepe*UVjBYEKhyz"), verify_certs=False)


