import pandas as pd
import numpy as np

from .api_requester import CryptoCompareRequester

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

    # TODO: Get only the ones with available symbols (relaxedValidation=False)
    df_fiat = pd.DataFrame.from_dict(ccrequester.get_symbols_price(tokenSymbols, relaxedValidation=True), orient='index')

    def _apply_values(row):
        if row['symbol'] in df_fiat.index:
            row['usdValue'] = row['balanceFloat'] * df_fiat.loc[row['symbol'], 'USD']
            row['ethValue'] = row['balanceFloat'] * df_fiat.loc[row['symbol'], 'ETH']
            row['eurValue'] = row['balanceFloat'] * df_fiat.loc[row['symbol'], 'EUR']
        else:
            row['usdValue'] = np.NaN
            row['ethValue'] = np.NaN
            row['eurValue'] = np.NaN
        
        return row

    df = df.apply(_apply_values, axis='columns')

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
        # TODO: Get only coins with available info (relaxedValidation=False)

        df = pd.DataFrame.from_dict(self.requester.get_symbols_price(tokenSymbols, relaxedValidation=True), orient='index')
        df.reset_index().to_feather(self.data_path)