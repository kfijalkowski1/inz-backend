from code.elastic_utils.utils import es_client
from typing import List

def get_index_for_id_containing(index: str, phrase: str) -> List[str]:
    """
    Get the ids of the index containing the phrase
    :param index: index name (eg. posts)
    :param phrase: phrase to look for
    :return: List of post ids
    """
    resp = es_client.search(index=index, query={"match": {"description": phrase}})
    return [x["_source"]["id"] for x in resp["hits"]["hits"]]


def get_posts_id_containing(phrase: str) -> List[str]:
    """
    Get the ids of the posts containing the phrase
    :param phrase:
    :return: List of post ids
    """
    return get_index_for_id_containing("posts", phrase)


def get_requests_id_containing(phrase: str) -> List[str]:
    """
    Get the ids of the requests containing the phrase
    :param phrase:
    :return: List of post ids
    """
    return get_index_for_id_containing("requests", phrase)