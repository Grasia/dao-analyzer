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


def n_requests(query: str, result_key: str, dao_id: str = '') -> List[Dict]:
    """
    Requests all chunks from endpoint.

    Parameters:
        * query: json to request
        * result_key 
        * dao_id
    """
    elements: List[Dict] = list()
    chunk: int = 0
    result = Dict
    condition: bool = True

    while condition:
        if dao_id:
            query_filled: str = query.format(dao_id, ELEMS_PER_CHUNK, len(elements))
        else:
            query_filled: str = query.format(ELEMS_PER_CHUNK, len(elements))

        result = request(query=query_filled)
        result = result[result_key]

        elements.extend(result)

        # if return data (result) has less than ELEMS_PER_CHUNK means that it was the last one 
        condition = len(result) == ELEMS_PER_CHUNK
        chunk += 1

    return elements
