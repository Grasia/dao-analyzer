import pandas as pd
import numpy as np

from cache_scripts.common.api_requester import CryptoCompareRequester

from .. import config
from .common import Collector, NetworkRunner

import logging

EMPTY_KEY_MSG = \
"""\
Empty CryptoCompare API key. You can obtain one from https://www.cryptocompare.com/cryptopian/api-keys
You can set the API key using --cc-api-key argument or the DAOA_CC_API_KEY env variable.
"""

def cc_postprocessor(df: pd.DataFrame) -> pd.DataFrame:
    ccrequester = CryptoCompareRequester(api_key=config.cc_api_key)

    tokenSymbols = df['symbol'].drop_duplicates()
    availableSymbols = {x['partner_symbol'] for x in ccrequester.get_available_coin_list()}
    tokenSymbols = availableSymbols.intersection(tokenSymbols)

    df_fiat = pd.DataFrame.from_dict(ccrequester.get_symbols_price(tokenSymbols), orient='index')

    cols = ['USD', 'ETH', 'EUR']

    df[cols] = np.NaN
    mask = df['symbol'].isin(df_fiat.index)
    df.loc[mask,cols] = df_fiat.loc[df[mask]['symbol'], cols].reset_index(drop=True).mul(df[mask]['balanceFloat'].reset_index(drop=True), axis=0).to_numpy()

    df = df.rename(columns={
        'USD': 'usdValue',
        'ETH': 'ethValue',
        'EUR': 'eurValue'
    })

    return df

class CCPricesCollector(Collector):
    def __init__(self, runner: NetworkRunner, name: str='tokenPrices'):
        super().__init__(name, runner)
        self.requester = CryptoCompareRequester(api_key=config.cc_api_key)

    def verify(self) -> bool:
        if not self.requester.api_key:
            logging.warning(EMPTY_KEY_MSG)
            return False

        return super().verify()
    
    @property
    def base(self):
        return self.runner.filterCollector(name='tokenBalances')

    def run(self, force=False, block=None):
        tokenSymbols = pd.read_feather(self.base.data_path, columns=['symbol']).drop_duplicates()['symbol']
        availableSymbols = {x['partner_symbol'] for x in self.requester.get_available_coin_list()}
        tokenSymbols = availableSymbols.intersection(tokenSymbols)

        df = pd.DataFrame.from_dict(self.requester.get_symbols_price(tokenSymbols), orient='index')
        df.reset_index().to_feather(self.data_path)