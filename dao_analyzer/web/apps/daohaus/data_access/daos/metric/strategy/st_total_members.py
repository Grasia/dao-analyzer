"""
   Descp: Strategy pattern to create total members.

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
import dao_analyzer.web.apps.daohaus.data_access.daos.metric.strategy.st_new_additions \
    as additions


class StTotalMembers(IMetricStrategy):

    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        pass


    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()
        
        members_data, rage_quits_data = self.__split_df(df=df)

        new_members: StackedSerie = additions.StNewAdditions(
            typ=additions.StNewAdditions.MEMBERS).process_data(members_data)

        out_members: StackedSerie = additions.StNewAdditions(
            typ=additions.StNewAdditions.OUTGOING_MEMBERS).process_data(rage_quits_data)

        total: List[int] = self.__calculate_total(
            new_members=new_members,
            out_members=out_members)

        s: Serie = Serie(x=new_members.get_serie()
            if len(new_members.get_serie()) >= len(out_members.get_serie())
            else out_members.get_serie())

        metric: StackedSerie = StackedSerie(
            serie = s, 
            y_stack = [total])

        return metric


    def __calculate_total(self, new_members: StackedSerie, out_members: StackedSerie) -> List[int]:
        total: List[int] = []
        
        news, outs = self.__adjust_lists(new_members, out_members)
        total.append(news[0] - outs[0])
        
        for i in range(1, len(news)):
            total.append(news[i] - outs[i] + total[i-1])

        return total


    def __split_df(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        rage_quits_data: pd.DataFrame = df.copy()
        members_data: pd.DataFrame = df.copy() if 'exists' in df.columns else pd.DataFrame() 

        if 'exists' in df.columns:
            # unique attr of member df
            members_data.loc[: ,:] = members_data[members_data.exists.notna()]
            members_data = members_data.dropna(how='all', axis=0)
            rage_quits_data.loc[: ,:] = rage_quits_data[rage_quits_data.exists.isna()]
            rage_quits_data = rage_quits_data.dropna(how='all', axis=0)

        return (members_data, rage_quits_data)


    def __adjust_lists(self, m_news: StackedSerie, 
    m_outs: StackedSerie) -> Tuple[List[int], List[int]]:

        news: List[int] = m_news.get_i_stack(0)
        outs: List[int] = m_outs.get_i_stack(0)

        s1: List = m_news.get_serie()
        s2: List = m_outs.get_serie()

        fill: List[int] = []

        if len(s1) > len(s2):
            fill = self.__fill_holes(s1=s1, s2=s2)
            outs = fill + outs

        elif len(s1) < len(s2):
            fill = self.__fill_holes(s1=s2, s2=s1)
            news = fill + news

        return (news, outs)


    def __fill_holes(self, s1: List, s2: List) -> List[int]:
        fill: List[int] = []

        for s in s1:
            if len(s2) > 0 and s == s2[0]:
                break
            fill.append(0)

        return fill
