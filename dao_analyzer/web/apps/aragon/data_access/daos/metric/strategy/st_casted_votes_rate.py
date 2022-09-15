"""
   Descp: Strategy pattern to create casted votes rate.

   Created on: 05-nov-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import pandas as pd
from typing import List

from dao_analyzer.web.apps.common.data_access.daos.metric.strategy import IMetricStrategy
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie
from dao_analyzer.web.apps.common.business.transfers.serie import Serie 
import dao_analyzer.web.apps.common.data_access.pandas_utils as pd_utl
from dao_analyzer.web.apps.aragon.data_access.daos.metric.strategy.st_cast_type \
    import StCastType


class StCastedVotesRate(IMetricStrategy):

    CAST_VOTE_FOR: int = 0
    CAST_VOTE_AGAINST: int = 1


    def __init__(self, m_type) -> None:
        self.__type = m_type


    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        pass


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()
        
        casts: StackedSerie = StCastType().process_data(df)

        rate: List[float] = self.__calculate_rate(m_casts=casts)

        metric: StackedSerie = StackedSerie(
            serie = Serie(x=casts.get_serie()), 
            y_stack = [rate])

        return metric


    def __calculate_rate(self, m_casts: StackedSerie) -> List[float]:
        rates: List[float] = []
        casts_for: List[int] = m_casts.get_i_stack(1)
        casts_against: List[int] = m_casts.get_i_stack(0)
        casts_type: List[int] = casts_against \
            if self.__type == self.CAST_VOTE_AGAINST else casts_for

        for i, _ in enumerate(casts_for):
            denominator: int = casts_for[i] + casts_against[i]
            rate: float = casts_type[i] / denominator if denominator else None
            rates.append(rate)

        return rates
