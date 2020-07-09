import json
from graphqlclient import GraphQLClient
from typing import Dict, List


ELEMS_PER_CHUNK: int = 1000
DAOSTACK_URL: str = 'https://api.thegraph.com/subgraphs/name/daostack/master'
client: GraphQLClient = GraphQLClient(DAOSTACK_URL)


def request(query: str) -> Dict:
    """
    Requests data from endpoint.
    """
    result = client.execute(query)
    result = json.loads(result)
    return result['data'] if 'data' in result else dict()


def n_requests(query: str, skip_n: int, result_key: str) -> List[Dict]:
    """
    Requests all chunks from endpoint.

    Parameters:
        * query: json to request
        * skip_n: number of rows to skip
        * result_key: dict key to access the list
    """
    elements: List[Dict] = list()
    result = Dict
    
    # do-while structure
    condition: bool = True

    while condition:
        query_filled: str = query.format(ELEMS_PER_CHUNK, skip_n + len(elements))

        result = request(query=query_filled)
        result = result[result_key]

        elements.extend(result)

        # if return data (result) has less than ELEMS_PER_CHUNK means that it was the last chunk 
        condition = len(result) == ELEMS_PER_CHUNK

    return elements
