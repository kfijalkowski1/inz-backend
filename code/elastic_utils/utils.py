from elasticsearch import Elasticsearch
import os

es_client = (
    Elasticsearch("http://localhost:9200/", basic_auth="elastic", verify_certs=False)
    if os.path.exists(".env") else
    Elasticsearch("http://elasticsearch-master.elk.svc.cluster.local:9200", basic_auth="elastic", verify_certs=False)
)


