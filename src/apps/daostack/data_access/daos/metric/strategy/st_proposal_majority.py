"""
   Descp: Strategy pattern for proposal's majority outcome

   Created on: 20-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""
import pandas as pd

from src.apps.daostack.data_access.daos.metric.strategy.\
        strategy_metric_interface import StrategyInterface
from src.apps.daostack.business.transfers.n_stacked_serie import NStackedSerie
from src.apps.daostack.business.transfers.stacked_serie import StackedSerie
from src.apps.daostack.business.transfers.serie import Serie
import src.apps.daostack.data_access.utils.pandas_utils as pd_utl


class StProposalMajority(StrategyInterface):
    __DF_DATE = 'executedAt'
    __DF_PASS = 'winningOutcome'
    __DF_REP = 'totalRepWhenExecuted'
    __DF_VOTES_F = 'votesFor'
    __DF_VOTES_A = 'votesAgainst'
    __DF_BOOST_AT = 'boostedAt'
    __DF_QUORUM = 'queuedVoteRequiredPercentage'
    __DF_INI_COLS = [__DF_DATE, __DF_PASS, __DF_REP, __DF_VOTES_F, __DF_VOTES_A,
                    __DF_BOOST_AT, __DF_QUORUM]

    __DF_MAJORITY_PER = 'majorityPer'
    __DF_IS_ABSOLUTE = 'isAbsolute'
    __DF_COLS = [__DF_DATE, __DF_PASS, __DF_MAJORITY_PER, __DF_IS_ABSOLUTE]


    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = df
        dff = dff.dropna(subset=[self.__DF_DATE]).copy()
        dff.loc[:, self.__DF_INI_COLS] = dff[self.__DF_INI_COLS]
        return dff


    def process_data(self, df: pd.DataFrame) -> NStackedSerie:
        if pd_utl.is_an_empty_df(df):
            return NStackedSerie()

        df = self.clean_df(df=df)
        df = self.__calculate_outcome(df=df)

        # takes just the month
        df = pd_utl.unix_to_date(df, self.__DF_DATE)
        df = pd_utl.transform_to_monthly_date(df, self.__DF_DATE)

        # generates a time serie
        idx = pd_utl.get_monthly_serie_from_df(df, self.__DF_DATE)

        # joinning all the data in a unique dataframe and fill with NA values
        dff = pd_utl.get_df_from_lists([idx, None, None, None], self.__DF_COLS)
        dff = pd_utl.datetime_to_date(dff, self.__DF_DATE)

        df = df.append(dff, ignore_index=True)
        #df.drop_duplicates(subset=self.__DF_DATE, keep="first", inplace=True)
        df.sort_values(self.__DF_DATE, inplace=True, ignore_index=True)

        return self.__generate_metric(df)


    def __generate_metric(self, df: pd.DataFrame) -> NStackedSerie:
        abs_passes, rel_passes = self.__get_sserie_outcome(df=df, has_pass=True)
        abs_fails, rel_fails = self.__get_sserie_outcome(df=df, has_pass=False)

        return NStackedSerie(sseries=[abs_passes, rel_passes, rel_fails, abs_fails])


    def __get_sserie_outcome(self, df: pd.DataFrame, has_pass: bool)\
    -> (StackedSerie, StackedSerie):

        # invert has_pass 'cause the df col has True, False and None values.
        dff: pd.DataFrame = pd_utl.filter_by_col_value(df, self.__DF_PASS, 
            (not has_pass), [pd_utl.NEQ])
        # absolute
        d3f: pd.DataFrame = pd_utl.filter_by_col_value(dff, self.__DF_IS_ABSOLUTE, 
            False, [pd_utl.NEQ])
        absolute: StackedSerie = self.__get_sserie_from_df(d3f)
        # relative
        d3f: pd.DataFrame = pd_utl.filter_by_col_value(dff, self.__DF_IS_ABSOLUTE, 
            True, [pd_utl.NEQ])
        relative: StackedSerie = self.__get_sserie_from_df(d3f)

        return (absolute, relative)


    def __get_sserie_from_df(self, df: pd.DataFrame) -> StackedSerie:
        serie: Serie = Serie(x=df[self.__DF_DATE].tolist())
        return StackedSerie(serie=serie, y_stack=[df[
            self.__DF_MAJORITY_PER].tolist()])

    
    def __calculate_outcome(self, df: pd.DataFrame) -> pd.DataFrame:
        dff: pd.DataFrame = pd_utl.get_empty_data_frame(self.__DF_COLS)

        for _, row in df.iterrows():
            total: int = int(row[self.__DF_REP])
            if total == 0:
                continue

            date: int = int(row[self.__DF_DATE])
            outcome: bool = True if row[self.__DF_PASS] == 'Pass' else False

            # boost == na means there was not boosted
            boost: bool = False if pd.isna(row[self.__DF_BOOST_AT]) else True

            percentage: int = (int(row[self.__DF_VOTES_F]) / total) if outcome \
                else (int(row[self.__DF_VOTES_A]) / total)
            percentage = round(percentage * 100, 1)

            is_absolute: bool  = True if int(row[self.__DF_QUORUM]) <= percentage else False

            has_passed: bool = False
            # winning outcome means more 'votes for' than 'votes against'
            if outcome:
                # it passed if outcome and it had relative majority or absolute majority 
                has_passed = boost or is_absolute

            dff = pd_utl.append_rows(dff, [date, has_passed, percentage, is_absolute])

        return dff
