"""
   Descp: Use this file in order to isolate your app logs

   Created on: 24-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

LOGS: dict = {
    'attr_not_init': 'You haven\'t initialized {} attribute\
, you can\'t use {} method directly.',
    'chunks_requested': 'Requested {} chunk(s) in {:.2f} ms',
    'daos_requested': '{} DAO(s) requested in {:.2f} s',
    'graph_error': 'An error has ocurred or no data available.',
    'no_attr_api_req': '\'args\' has to be filled with a query.\n',
    'no_attr_cache_req': '\'args\' has to be filled with a cache path.\n',
    'request_to': 'Requesting to: {}',
    'requested_in': 'Requested in {:.2f} ms',
}