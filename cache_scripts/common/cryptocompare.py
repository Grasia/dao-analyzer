import pandas as pd

from cache_scripts.common.api_requester import CryptoCompareRequester

from .common import Collector

class CCPricesCollector(Collector):
    def __init__(self, runner, name: str='tokenPrices'):
        super().__init__(name, runner)
        self.requester = CryptoCompareRequester()
    
    @property
    def base(self):
        return self.runner.filterCollector(name='tokenBalances')

    def run(self, force=False, block=None):
        tokenSymbols = pd.read_feather(self.base.data_path, columns='symbol').drop_duplicates()
        availableSymbols = self.requester.get_available_coin_list()
        tokenSymbols = availableSymbols[availableSymbols.isin(tokenSymbols)]

        df = pd.DataFrame.from_dict(self.requester.get_symbols_price(tokenSymbols), orient='index')
        df.reset_index().to_feather(self.data_path)