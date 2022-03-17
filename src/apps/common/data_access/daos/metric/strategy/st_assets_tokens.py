import pandas as pd

from . import IMetricStrategy
from .....business.transfers import TabularData

class StAssetsTokens(IMetricStrategy):
    __GB_COLUMNS = ['network', 'symbol']
    __ALLOWED_COLUMNS = __GB_COLUMNS + ['balanceFloat']
    __VALUE_COLUMN = 'usdValue'

    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        mask = ~(df[self.__VALUE_COLUMN] > 0)
        return df[mask][self.__ALLOWED_COLUMNS]

    def process_data(self, df: pd.DataFrame) -> TabularData:
        df = self.clean_df(df)

        dfg = df.groupby(self.__GB_COLUMNS)
        columns = {
            'network': 'Network',
            'symbol': 'Symbol',
            'balanceFloat': 'Balance'
        }

        return TabularData.from_df(dfg.sum()).set_column_names(columns)