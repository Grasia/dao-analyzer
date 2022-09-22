"""
   Descp: Strategy pattern to create the percentage of voters from all the users.

   Created on: 05-nov-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import pandas as pd
from typing import List, Tuple

from dao_analyzer.web.apps.common.data_access.daos.metric.strategy import IMetricStrategy
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie
from dao_analyzer.web.apps.common.business.transfers.serie import Serie 
import dao_analyzer.web.apps.common.data_access.pandas_utils as pd_utl
import dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.st_total_reputation_holders \
    as reputation_holders
import dao_analyzer.web.apps.daostack.data_access.daos.metric.strategy.st_different_voters_stakers \
    as m_voters


class StVotersPercentage(IMetricStrategy):

    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        pass


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()
        
        holders_data, vote_data = self.__split_df(df)

        holders: StackedSerie = reputation_holders.StTotalRepHolders()\
            .process_data(df=holders_data)

        voters: StackedSerie = m_voters.StDifferentVS(m_type=m_voters.VOTERS)\
            .process_data(df=vote_data)

        percentage: List[float] = self.__calculate_percentage(
            m_holders=holders,
            m_voters=voters)

        s: Serie = Serie(x=holders.get_serie()
            if len(holders.get_serie()) >= len(voters.get_serie())
            else voters.get_serie())

        metric: StackedSerie = StackedSerie(
            serie = s, 
            y_stack = [percentage])

        return metric


    def __split_df(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        holders_data: pd.DataFrame = df
        vote_data: pd.DataFrame = df.copy() if 'voter' in df.columns else pd.DataFrame()

        if 'voter' in df.columns:
            # attr of vote df
            vote_data.loc[: ,:] = vote_data[vote_data.voter.notna()]
            vote_data = vote_data.dropna(how='all', axis=0)
            holders_data.loc[: ,:] = holders_data[holders_data.voter.isna()]
            holders_data = holders_data.dropna(how='all', axis=0)

        return (holders_data, vote_data)


    def __calculate_percentage(self, m_holders: StackedSerie, 
    m_voters: StackedSerie) -> List[float]:

        percentage: List[float] = []
        holders, voters = self.__adjust_lists(m_holders, m_voters)

        for i, _ in enumerate(holders):
            numerator: int = voters[i]
            denominator: int = holders[i]

            percentage.append(
                round(numerator / denominator * 100, 4) if denominator else None
            )

        return percentage


    def __adjust_lists(self, m_holders: StackedSerie, 
    m_voters: StackedSerie) -> Tuple[List[int], List[int]]:

        holders: List[int] = m_holders.get_i_stack(0)
        voters: List[int] = m_voters.get_i_stack(0)

        s1: List = m_holders.get_serie()
        s2: List = m_voters.get_serie()

        fill: List[int] = []

        if len(s1) > len(s2):
            fill = self.__fill_holes(s1=s1, s2=s2)
            voters = fill + voters

        elif len(s1) < len(s2):
            fill = self.__fill_holes(s1=s2, s2=s1)
            holders = fill + holders

        return (holders, voters)


    def __fill_holes(self, s1: List, s2: List) -> List[int]:
        fill: List[int] = []

        for s in s1:
            if len(s2) > 0 and s == s2[0]:
                break
            fill.append(0)

        return fill
