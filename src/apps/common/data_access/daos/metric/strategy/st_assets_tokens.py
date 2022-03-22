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
        df['cnt'] = 1

        dfg = df.groupby(self.__GB_COLUMNS)
        columns = {
            'network': 'Network',
            'symbol': 'Symbol',
            'balanceFloat': 'Total Balance',
            'cnt': '# DAOs holding',
        }

        sum = dfg.sum()

        # Remove the cnt if they are all from the same DAO
        if (sum['cnt'] == 1).all():
            sum = sum.drop(columns='cnt')
        
        return TabularData.from_df(sum).set_column_names(columns)