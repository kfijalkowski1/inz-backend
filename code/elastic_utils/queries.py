from code.elastic_utils.utils import es_client
from typing import List

def get_posts_id_containing(phrase: str) -> List[str]:
    """
    Get the ids of the posts containing the phrase
    :param phrase:
    :return: List of post ids
    """
    resp = es_client.search(index="posts", query={"match": {"description": phrase}})
    return [x["_source"]["id"] for x in resp["hits"]["hits"]]