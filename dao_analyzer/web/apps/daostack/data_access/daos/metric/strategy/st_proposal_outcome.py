"""
   Descp: Strategy pattern for proposal's boost outcomes in a timeline 

   Created on: 13-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Tuple, Any
import pandas as pd

from dao_analyzer.web.apps.common.data_access.daos.metric.strategy import IMetricStrategy
from dao_analyzer.web.apps.common.business.transfers.stacked_serie import StackedSerie
from dao_analyzer.web.apps.common.business.transfers.n_stacked_serie import NStackedSerie 
from dao_analyzer.web.apps.common.business.transfers.serie import Serie
import dao_analyzer.web.apps.common.data_access.pandas_utils as pd_utl


BOOST_OUTCOME: int = 0
BOOST_SUCCESS_RATIO: int = 1
TOTAL_SUCCESS_RATIO: int = 2


class StProposalOutcome(IMetricStrategy):
    __DF_DATE = 'executedAt'
    __DF_PASS = 'hasPassed'
    __DF_BOOST = 'isBoosted'
    __DF_BOOST_AT = 'boostedAt'
    __DF_OUTCOME = 'winningOutcome'
    __DF_REP = 'totalRepWhenExecuted'
    __DF_VOTES_F = 'votesFor'
    __DF_QUORUM = 'queuedVoteRequiredPercentage'
    __DF_COUNT = 'count'
    __DF_COLS1 = [__DF_DATE, __DF_PASS, __DF_BOOST]
    __DF_COLS2 = [__DF_DATE, __DF_PASS, __DF_BOOST, __DF_COUNT]
    __DF_INI_COLS = [__DF_DATE, __DF_OUTCOME, __DF_REP, __DF_VOTES_F,
                    __DF_BOOST_AT, __DF_QUORUM]


    def __init__(self, m_type: int):
        self.__m_type = m_type


    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = df
        dff = dff.dropna(subset=[self.__DF_DATE])
        dff.loc[:, self.__DF_INI_COLS] = dff[self.__DF_INI_COLS]
        return dff


    def __get_boost_from_dataframe(self, df: pd.DataFrame, boosted: bool)\
    -> Tuple[List[int]]:
        s_pass: List[int] = list()
        s_not_pass: List[int] = list()

        boost: List[int] = df[self.__DF_BOOST].tolist()
        is_pass: List[int] = df[self.__DF_PASS].tolist()
        count: List[int] = df[self.__DF_COUNT].tolist()

        for i, b in enumerate(boost):
            if b == boosted:
                if is_pass[i]:
                    s_pass.append(count[i])
                else:
                    s_not_pass.append(count[i])

        return (s_not_pass, s_pass)


    def __get_empty_transfer(self) -> Any:
        if self.__m_type == BOOST_OUTCOME:
            return StackedSerie()
        elif self.__m_type == TOTAL_SUCCESS_RATIO:
            return StackedSerie()
        elif self.__m_type == BOOST_SUCCESS_RATIO:
            return NStackedSerie()

        return None


    def process_data(self, df: pd.DataFrame) -> Any:
        if pd_utl.is_an_empty_df(df):
            return self.__get_empty_transfer()

        df = self.clean_df(df=df)
        df = self.__calculate_outcome(df=df)

        # takes just the month
        df = pd_utl.unix_to_date(df, self.__DF_DATE)
        df = pd_utl.transform_to_monthly_date(df, self.__DF_DATE)

        df = pd_utl.count_cols_repetitions(df=df, 
            cols=self.__DF_COLS1, new_col=self.__DF_COUNT)

        # generates a time serie
        idx = pd_utl.get_monthly_serie_from_df(df, self.__DF_DATE)

        # joinning all the data in a unique dataframe and fill with all combinations
        for p in [True, False]:
            for b in [True, False]:
                dff = pd_utl.get_df_from_lists([idx, p, b, 0], self.__DF_COLS2)

                dff = pd_utl.datetime_to_date(dff, self.__DF_DATE)
                df = pd.concat([df, dff], ignore_index=True)

        df = df.drop_duplicates(subset=self.__DF_COLS1, keep="first")
        df = df.sort_values(self.__DF_DATE, ignore_index=True)

        return self.generate_metric(df)


    def generate_metric(self, df: pd.DataFrame) -> Any:
        metric = StackedSerie()

        if self.__m_type == BOOST_OUTCOME:
            metric = self.__get_boost_outcome(df)
        elif self.__m_type == TOTAL_SUCCESS_RATIO:
            metric = self.__get_total_success_ratio(df)
        elif self.__m_type == BOOST_SUCCESS_RATIO:
            metric = self.__get_boost_success_ratio(df)

        return metric


    def __get_boost_outcome(self, df: pd.DataFrame) -> StackedSerie:
        serie: Serie = Serie(x = df.drop_duplicates(subset=self.__DF_DATE,
            keep="first")[self.__DF_DATE].tolist())

        n_p1, p1 = self.__get_boost_from_dataframe(df, boosted=False)
        n_p2, p2 = self.__get_boost_from_dataframe(df, boosted=True)

        return StackedSerie(serie=serie, y_stack=[p1, p2, n_p2, n_p1])


    def __get_total_success_ratio(self, df: pd.DataFrame) -> StackedSerie:
        serie: Serie = Serie(x = df.drop_duplicates(subset=self.__DF_DATE,
            keep="first")[self.__DF_DATE].tolist())

        tp: List[int] = self.__get_predicted_values(df, 'tp')
        tn: List[int] = self.__get_predicted_values(df, 'tn')
        fp: List[int] = self.__get_predicted_values(df, 'fp')
        fn: List[int] = self.__get_predicted_values(df, 'fn')

        ratio: List[float] = self.__calculate_ratio(
            numerator=[tp, tn], 
            denominator=[tp, tn, fp, fn], 
            _len=len(tp))

        return StackedSerie(serie=serie, y_stack=[ratio])


    def __get_boost_success_ratio(self, df: pd.DataFrame) -> NStackedSerie:
        serie: Serie = Serie(x = df.drop_duplicates(subset=self.__DF_DATE,
            keep="first")[self.__DF_DATE].tolist())

        tp: List[int] = self.__get_predicted_values(df, 'tp')
        tn: List[int] = self.__get_predicted_values(df, 'tn')
        fp: List[int] = self.__get_predicted_values(df, 'fp')
        fn: List[int] = self.__get_predicted_values(df, 'fn')

        boost_ratio: List[float] = self.__calculate_ratio(
            numerator=[tp], 
            denominator=[tp, fp], 
            _len=len(tp))

        nboost_ratio: List[float] = self.__calculate_ratio(
            numerator=[tn], 
            denominator=[tn, fn], 
            _len=len(tn))

        return NStackedSerie(
            serie=serie, 
            sseries=[
                StackedSerie(y_stack=[boost_ratio]),
                StackedSerie(y_stack=[nboost_ratio])])


    def __calculate_ratio(self, numerator: List, denominator: List, 
    _len: int) -> List:

        ratio: List = list()
        for i in range(_len):
            n_val: int = 0
            d_val: int = 0

            # numerator elements sum
            for n in numerator:
                n_val += n[i]

            # denominator elements sum
            for d in denominator:
                d_val += d[i]

            if d_val == 0:
                ratio.append(None)
            else:
                ratio.append(round(n_val / d_val, 4))

        return ratio

    
    def __calculate_outcome(self, df: pd.DataFrame) -> pd.DataFrame:
        df[self.__DF_BOOST] = ~pd.isna(df[self.__DF_BOOST_AT])
        df[self.__DF_PASS] = df.apply(lambda r: self.__has_passed(r, r[self.__DF_BOOST]), axis='columns')
        df = df.filter(self.__DF_COLS1).astype(object)
        return df


    def __has_passed(self, data, is_boost: bool) -> bool:
        # winning outcome means more votes for than votes against
        outcome: bool = data[self.__DF_OUTCOME] == 'Pass'
        percentage = int(data[self.__DF_VOTES_F]) / int(data[self.__DF_REP]) * 100 \
            if int(data[self.__DF_REP]) > 0 else 0
        limit: int = int(data[self.__DF_QUORUM])

        has_passed: bool = outcome and is_boost
        # if there was no boost and pass outcome, you must consider if there was absolute majority
        if outcome and not is_boost:
            has_passed = percentage >= limit

        return has_passed


    def __get_predicted_values(self, df: pd.DataFrame, pred: str) -> List[int]:
        """ 
        True positives = boost and pass
        True negatives = not boost and not pass
        False positives = boost and not pass
        False negatives = not boost and pass

        Parameters:
            * df = data frame to filter
            * pred = must be 'tp', 'tn', 'fp', 'fn' in other case return true 
                     positive by default.
        Return:
            A list with a counter of predicted values. This list has the 
            number of elements such as different dates of the df parameter.
            This list is also ordered by the dates of the df parameter. 
        """
        # default tp
        boost: bool = True
        _pass: bool = True

        if pred == 'tn':
            boost = False
            _pass = False
        elif pred == 'fp':
            _pass = False
        elif pred == 'fn':
            boost = False

        dff = pd_utl.filter_by_col_value(df, self.__DF_BOOST, boost, [pd_utl.EQ])
        dff = pd_utl.filter_by_col_value(dff, self.__DF_PASS, _pass, [pd_utl.EQ])

        # date reconstruction
        idx = pd_utl.get_monthly_serie_from_df(dff, self.__DF_DATE)
        d3f = pd_utl.get_df_from_lists([idx, 0], [self.__DF_DATE, self.__DF_COUNT])
        d3f = pd_utl.datetime_to_date(d3f, self.__DF_DATE)

        dff = pd_utl.filter_by_col_value(dff, self.__DF_COUNT, 0, [pd_utl.GT])
        dff = dff.drop(columns=[self.__DF_BOOST, self.__DF_PASS])

        dff = pd.concat([dff, d3f], ignore_index=True)
        dff = dff.drop_duplicates(subset=self.__DF_DATE, keep="first")
        dff = dff.sort_values(self.__DF_DATE, ignore_index=True)

        return dff[self.__DF_COUNT].to_list()
    