from multiprocessing.sharedctypes import Value
import pandas as pd
import requests
import logging
from functools import partial
from tqdm import tqdm
from time import sleep
from typing import Union

import numpy as np

from ..metadata import Block

from . import ENDPOINTS
from .common import NetworkCollector
from .graphql import GraphQLCollector

MSG_NO_TOKENS_FOUND = "No tokens found"

class BlockscoutBallancesCollector(NetworkCollector):
    TMR_SLEEP = 60

    def __init__(self, runner, base: GraphQLCollector, name: str='tokenBalances', network: str='mainnet', addr_key: str='id'):
        """ Initializes a ballance collector that uses blockscout
        
        Parameters:
            name (str): The name of the collector (and filename)
            runner (Runner): The runner in which it's based
            network (str): The network to run on
            base (GraphQLCollector): The DAOs/organizations collector to get the DAO list from
            index_key (str): The key to use to access the address in the base array
        """
        super().__init__(name, runner, network)
        self.base = base
        self.addr_key = addr_key

    @property
    def endpoint(self) -> str:
        return ENDPOINTS[self.network]['blockscout']

    def _get_from_address(self, addr: str, retry: int = 0, maxretries: int = 3, block: Union[int, Block] = None) -> pd.DataFrame:
        if retry >= maxretries:
            raise ValueError(f"Too many retries {retry}/{maxretries}")

        blockn = block
        if blockn is None:
            blockn = 'latest'
        elif isinstance(blockn, Block):
            blockn = blockn.number

        r = requests.get(ENDPOINTS[self.network]['blockscout'], params={
            'module': 'account',
            'action': 'tokenlist',
            'block': blockn,
            'address': addr
        })

        if (r.ok):
            j = r.json()
            if j['status'] == str(1) and j['message'] == 'OK':
                df = pd.DataFrame(j['result'])
                # Only ERC-20 tokens (not NFTs or others)
                df = df[df.type == 'ERC-20']
                df = df.replace(r'^\s*$', np.nan, regex=True)
                df = df.dropna()

                # Calculate decimals
                df['decimals'] = df['decimals'].astype(int)
                df['balanceFloat'] = df['balance'].astype(float) / (10 ** df['decimals'])

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
        elif r.status_code == 429: # Too many requests
            logging.warning(f"Too many requests, sleep and retry {retry}/{maxretries} time")
            sleep(self.TMR_SLEEP)
            return self._get_from_address(addr, retry=retry+1, maxretries=maxretries)
        elif r.status_code == 504: # Gateway Time-out (Response too large)
            logging.warning(f"Requests returned Gateway Time-out, ignoring response for addr {addr}")
            return pd.DataFrame() 
        else:
            logging.error(f"Requests failed with status code {r.status_code}: {r.reason}")
            raise ValueError(f"Requests failed with status code {r.status_code}: {r.reason}")

    def run(self, force=False, block: Block = None):
        # For each of the DAOs in the df, get the token balance
        addresses = self.base.df[self.addr_key].drop_duplicates()

        if addresses.empty:
            logging.warning("No addresses returned, not running blockscout collector")
            return

        ptqdm = partial(tqdm, delay=1, desc="Requesting token balances", 
            unit='req', dynamic_ncols=True)
        toApply = partial(self._get_from_address, block=block)
        df = pd.concat(map(toApply, ptqdm(addresses)), ignore_index=True)
        
        self._update_data(df, force)