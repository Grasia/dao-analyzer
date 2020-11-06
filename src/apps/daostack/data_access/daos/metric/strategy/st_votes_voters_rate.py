"""
   Descp: Strategy pattern to create votes-voters rate.

   Created on: 04-nov-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import pandas as pd
from typing import List

from src.apps.common.data_access.daos.metric.imetric_strategy \
    import IMetricStrategy
from src.apps.common.business.transfers.stacked_serie import StackedSerie
from src.apps.common.business.transfers.serie import Serie 
import src.apps.common.data_access.pandas_utils as pd_utl
import src.apps.daostack.data_access.daos.metric.strategy.st_time_serie \
    as vote_metric
import src.apps.daostack.data_access.daos.metric.strategy.st_different_voters_stakers \
    as voters_metric


class StVoteVotersRate(IMetricStrategy):

    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        pass


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()
        
        votes: StackedSerie = vote_metric\
            .StTimeSerie(m_type=vote_metric.TOTAL_VOTES).process_data(df.copy())
        voters: StackedSerie = voters_metric\
            .StDifferentVS(m_type=voters_metric.VOTERS).process_data(df)

        rate: List[float] = self.__calculate_rate(
            m_votes=votes,
            m_voters=voters
        )

        metric: StackedSerie = StackedSerie(
            serie = Serie(x=votes.get_serie()), 
            y_stack = [rate])

        return metric


    def __calculate_rate(self, m_votes: StackedSerie, m_voters: StackedSerie) -> List[float]:
        rates: List[float] = []

        votes: List[int] = m_votes.get_i_stack(0)
        voters: List[int] = m_voters.get_i_stack(0)

        for i, _ in enumerate(votes):
            rate: float = round(votes[i] / voters[i], 2) if votes[i] else None
            rates.append(rate)

        return rates