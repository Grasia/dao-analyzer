import pandas as pd

from cache_scripts.common.api_requester import CryptoCompareRequester

from .. import config
from .common import Collector, NetworkRunner

import logging

EMPTY_KEY_MSG = \
"""\
Empty CryptoCompare API key. You can obtain one from https://www.cryptocompare.com/cryptopian/api-keys
You can set the API key using --cc-api-key argument or the DAOA_CC_API_KEY env variable.
"""

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