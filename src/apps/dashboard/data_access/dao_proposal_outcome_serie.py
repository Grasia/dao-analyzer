"""
   Descp: This is a dao (data access object) of stacked series and for 
    the specific purpose to calculate proposals type's outcomes.
    It's used in order to warp the transformation among
    API's responses and the App's transfer.  

   Created on: 4-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui 
        <f.r.youssef@hotmail.com>
"""

from typing import List, Dict, Tuple
from pandas.tseries.offsets import DateOffset
from datetime import datetime
import pandas as pd

from src.app import DEBUG
from src.logs import LOGS
from src.apps.dashboard.business.transfers.serie import Serie
from src.apps.dashboard.business.transfers.stacked_serie import StackedSerie
from src.api.query import Query
from src.api.query_builder import QueryBuilder
import src.api.api_manager as api


def __apend_json_data(columns: List[str], new_data: List[Dict[str, str]])\
 -> pd.DataFrame:
    """
    Takes new_data elements and joins them into df which is returned.
    """
    df: pd.DataFrame = pd.DataFrame(columns = columns)
    boost: List[str] = ['BoostedTimeOut', 'BoostedBarCrossed']

    for di in new_data:
        x: int = None if di['closingAt'] == 'null' else int(di['closingAt'])
        y: bool = True if di['winningOutcome'] == 'Pass' else False
        z: bool = True if any(x == di['executionState'] for x in boost)\
            else False

        # just append closed proposals
        if x:
            serie: pd.Series = pd.Series([x, y, z], index = df.columns)
            df = df.append(serie, ignore_index=True)

    return df

def __request(o_id: str, columns: List[str]) -> pd.DataFrame:
    """
    Requests data and returns a pandas dataframe with columns distribution.
    Params:
        * o_id = An organization id
        * columns = Columns name for returned dataframe structure
    Return:
        * A pandas dataframe
    """
    chunk: int = 0
    result: Dict[str, List] = dict()
    df: pd.DataFrame = pd.DataFrame(columns = columns)
    start: datetime = datetime.now()

    while chunk == 0 or ('dao' in result and \
    len(result['dao']['proposals']) == api.get_elems_per_chunk(chunk - 1)):

        q_builder: QueryBuilder = QueryBuilder()
        query: Query = Query(header = 'dao',
                            body = Query(
                                        header = 'proposals',
                                        body = ['closingAt', 'executionState',\
                                         'winningOutcome'],
                                        filters = {
                                            'first': 
                                            f'{api.get_elems_per_chunk(chunk)}',
                                            'skip' : f'{df.shape[0]}',
                                        },
                                    ),
                            filters = {
                                'id': f'\"{o_id}\"',
                            })

        q_builder.add_query(query)
        result = api.request(q_builder.build())
        dff: pd.DataFrame = __apend_json_data(columns = columns,\
             new_data = result['dao']['proposals'])
        df = df.append(dff, ignore_index = True)
        chunk += 1

    if DEBUG:
        print(LOGS['chunks_requested'].format(chunk, (datetime.now() - start)\
         .total_seconds() * 1000))

    return df


def __get_stacked_serie_from_dataframe(df: pd.DataFrame, boosted: bool)\
    -> Tuple[List[int]]:

    s_pass: List[int] = list()
    s_not_pass: List[int] = list()

    for _, row in df.iterrows():
        if row['isBoosted'] == boosted:
            if row['hasPassed']:
                s_pass.append(row['count'])
            else:
                s_not_pass.append(row['count'])

    return (s_not_pass, s_pass)


def __process_data(df: pd.DataFrame) -> StackedSerie:
    if df.shape[0] == 0:
        return StackedSerie()

    # takes just the month
    df['closedAt'] = pd.to_datetime(df['closedAt'], unit='s').dt.to_period('M')

    # groupby columns and count repetitions as a new column.
    df = df.groupby(['closedAt', 'hasPassed', 'isBoosted']).size().reset_index(name='count')
    df['closedAt'] = df['closedAt'].dt.to_timestamp()
    
     # generates a time serie
    today = datetime.now()
    today = datetime(today.year, today.month, 1)
    start = df['closedAt'].min() if len(df['closedAt']) > 0 else today 
    end = today
    idx = pd.date_range(start=start, end=end, freq=DateOffset(months=1))

    # joinning all the data in a unique dataframe and fill with all combinations
    for p in [True, False]:
        for b in [True, False]:
            dff = pd.DataFrame({
                'closedAt': idx,
                'hasPassed': p,
                'isBoosted': b,
                'count': 0})
            df = df.append(dff, ignore_index = True)

    df.drop_duplicates(subset = ['closedAt', 'hasPassed', 'isBoosted'],
     keep = "first", inplace = True)
    df.sort_values('closedAt', inplace = True, ignore_index = True)

    # generate metric output
    serie: Serie = Serie(x = df.drop_duplicates(subset = 'closedAt', \
        keep = "first")['closedAt'].tolist())

    n_p1, p1 = __get_stacked_serie_from_dataframe(df, False)
    n_p2, p2 = __get_stacked_serie_from_dataframe(df, True)

    return StackedSerie(serie = serie, y_stack = [p1, p2, n_p2, n_p1])


def get_metric(ids: List[str]) -> StackedSerie:
    """
    Gets a n times stacked serie from a list of ids.
    Params:
        ids: a list of existing DAO's id.
    Return:
        StackedSerie
    """
    start: datetime = datetime.now()
    df: pd.DataFrame = pd.DataFrame(columns = ['closedAt', 'hasPassed',
     'isBoosted'])

    for o_id in ids:
        dff: pd.DataFrame = __request(o_id = o_id, columns = df.columns)
        df = df.append(dff, ignore_index = True)

    if DEBUG:
        duration: int = (datetime.now() - start).total_seconds()
        print(LOGS['daos_requested'].format(len(ids), duration))

    return __process_data(df)