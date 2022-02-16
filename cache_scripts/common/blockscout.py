import pandas as pd
import requests
import logging
from functools import partial
from tqdm import tqdm

from ..metadata import Block

from . import ENDPOINTS
from .common import Collector
from .graphql import GraphQLCollector

MSG_NO_TOKENS_FOUND = "No tokens found"

class BlockscoutBallancesCollector(Collector):
    def __init__(self, runner, base: GraphQLCollector, name: str='tokenBalances', network: str='mainnet', addr_key: str='id'):
        """ Initializes a ballance collector that uses blockscout
        
        Parameters:
            name (str): The name of the collector (and filename)
            runner (Runner): The runner in which it's based
            network (str): The network to run on
            base (GraphQLCollector): The DAOs/organizations collector to get the DAO list from
            index_key (str): The key to use to access the address in the base array
        """
        super().__init__(name, runner)
        self.base = base
        self.network = network
        self.addr_key = addr_key

    @property
    def endpoint(self) -> str:
        return ENDPOINTS[self.network]['blockscout']

    def _get_from_address(self, addr: str) -> pd.DataFrame:
        r = requests.get(ENDPOINTS[self.network]['blockscout'], params={
            'module': 'account',
            'action': 'tokenlist',
            'address': addr
        })

        if (r.ok):
            j = r.json()
            if j['status'] == str(1) and j['message'] == 'OK':
                df = pd.DataFrame(j['result'])
                # Only ERC-20 tokens (not NFTs or others)
                df = df[df.type == 'ERC-20']

                # Calculate decimals
                df['decimals'] = df['decimals'].astype(int)
                df['balanceFloat'] = df['balance'].astype(float) / 10 ** df['decimals']

                # Add index
                df['address'] = addr
                df['network'] = self.network
                df['id'] = 'token-' + df['contractAddress'] + '-org-' + df['address']
                return df
            elif j['message'] == MSG_NO_TOKENS_FOUND:
                return pd.DataFrame()
            else:
                logging.warning(f"Status {j['status']}, message: {j['message']}")
                return pd.DataFrame()
        else:
            logging.error(f"Requests failed with status code {r.status_code} {r.reason}")
            raise ValueError()

    def run(self, force=False, block: Block = None):
        # For each of the DAOs in the df, get the token balance
        ptqdm = partial(tqdm, delay=1, desc="Requesting token balances", 
            unit='req', dynamic_ncols=True)
        df = pd.concat(map(self._get_from_address, ptqdm(self.base.df[self.addr_key])))
        
        self._update_data(df, force)