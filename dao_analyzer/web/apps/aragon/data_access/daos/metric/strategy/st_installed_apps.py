"""
   Descp: Strategy pattern to create a metric of installed apps.

   Created on: 20-oct-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import pandas as pd
from typing import List

from dao_analyzer.web.apps.common.data_access.daos.metric.strategy import IMetricStrategy
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie
from dao_analyzer.web.apps.common.business.transfers.serie import Serie
import dao_analyzer.web.apps.common.data_access.pandas_utils as pd_utl


class StInstalledApps(IMetricStrategy):
    __MAX_APPS: int = 15
    __OTHERS: str = 'Others'
    __DF_ID: str = 'id'
    __DF_NAME: str = 'repoName'
    __DF_COUNT: str = 'count'
    __DF_COLS: List[str] = [__DF_ID, __DF_NAME]


    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = df
        dff.loc[:, self.__DF_COLS] = dff[self.__DF_COLS]
        return dff


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()
        
        df = self.clean_df(df=df)

        # count pair id-name
        df = pd_utl.count_cols_repetitions(df, self.__DF_COLS, self.__DF_COUNT)

        #remove apps which has not name
        df = df.dropna(subset=[self.__DF_NAME])

        # count name repetitions (should be repoAddress, however not all of them have an entry)
        df = pd_utl.count_cols_repetitions(df, [self.__DF_NAME], self.__DF_COUNT)
        df = df.sort_values(self.__DF_COUNT, ascending=False)

        df = self.__adjust_values(df=df)

        serie: Serie = Serie(x=df[self.__DF_NAME].tolist())
        metric: StackedSerie = StackedSerie(
            serie = serie, 
            y_stack = [df[self.__DF_COUNT].tolist()])

        return metric


    def __adjust_values(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = df
        
        if len(dff) <= self.__MAX_APPS:
            return dff

        names: List[str] = dff[self.__DF_NAME].tolist()[:self.__MAX_APPS]
        installs: List[str] = dff[self.__DF_COUNT].tolist()[:self.__MAX_APPS]
        
        # add the sum of the others
        names.append(self.__OTHERS)
        other_installs: List[str] = dff[self.__DF_COUNT].tolist()[self.__MAX_APPS:]
        installs.append(sum(other_installs))

        return pd.DataFrame(
            {
                self.__DF_NAME: names,
                self.__DF_COUNT: installs
            })
