"""
   Descp: Manage the application logic, and it's used to interconect the
        data_access and presentation layers.

   Created on: 2-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List, Callable
import dash_html_components as html

import src.apps.common.presentation.dashboard_view as view
from src.apps.common.data_access.daos.organization_dao\
    import OrganizationListDao
import src.apps.aragon.data_access.requesters.cache_requester as cache
from src.apps.common.business.transfers.organization import OrganizationList
from src.apps.common.presentation.charts.chart_controller import ChartController
from src.apps.common.presentation.charts.layout.chart_pane_layout \
    import ChartPaneLayout
from src.apps.common.presentation.charts.layout.figure.figure import Figure
from src.apps.common.presentation.charts.layout.figure.bar_figure import BarFigure
# from src.apps.common.presentation.charts.layout.figure.multi_bar_figure import MultiBarFigure
import src.apps.aragon.data_access.daos.metric.metric_dao_factory as s_factory
from src.apps.common.business.i_metric_adapter import IMetricAdapter
from src.apps.aragon.business.metric_adapter.basic_adapter import BasicAdapter
from src.apps.aragon.business.metric_adapter.installed_apps import InstalledApps 

from src.apps.aragon.resources.strings import TEXT
from src.apps.common.resources.strings import TEXT as COMMON_TEXT
import src.apps.common.resources.colors as COLOR


_aragon_service = None

def get_service():
    """
    Singelton object.
    """
    global _aragon_service

    if not _aragon_service:
        _aragon_service = AragonService()

    return _aragon_service


class AragonService():
    _TOKEN_HOLDER: int = 0
    _VOTE: int = 1
    _CAST: int = 2
    _TRANSACTION: int = 3
    _APP: int = 4

    def __init__(self):
        # app state
        self.__orgs: OrganizationList = None
        self.__controllers: Dict[int, List[ChartController]] = {
            self._TOKEN_HOLDER: list(),
            self._VOTE: list(),
            self._CAST: list(),
            self._TRANSACTION: list(),
            self._APP: list(),
        }


    @property
    def organizations(self) -> OrganizationList:
        if not self.__orgs:
            orgs: OrganizationList = OrganizationListDao(cache.CacheRequester(
                srcs=[cache.ORGANIZATIONS])).get_organizations()
            if not orgs.is_empty():
                self.__orgs = orgs
                
        return self.__orgs


    @property
    def are_panes(self) -> bool:
        """
        Checks if panes and their controllers are already created.
        """
        is_empty: bool = False

        for _, v in self.__controllers.items():
            is_empty = is_empty or (len(v) != 0)

        return is_empty


    def get_layout(self) -> html.Div:
        """
        Returns the app's layout. 
        """
        orgs: OrganizationList = self.organizations
        return view.generate_layout(
            labels=orgs.get_dict_representation(),
            sections=self.__get_sections(),
            color_app=COMMON_TEXT['css_color_aragon']
        )


    def __get_sections(self) -> Dict[str, List[Callable]]:
        """
        Returns a dict with each section filled with a callable function which
         returns the chart layout
        """
        l_token_holders: List[Callable] = list()
        l_vote: List[Callable] = list()
        l_cast: List[Callable] = list()
        l_transaction: List[Callable] = list()
        l_app: List[Callable] = list()

        # Panes are already created.
        if self.are_panes:
            l_token_holders = [c.layout.get_layout for c in self.__controllers[self._TOKEN_HOLDER]]
            l_vote = [c.layout.get_layout for c in self.__controllers[self._VOTE]]
            l_cast = [c.layout.get_layout for c in self.__controllers[self._CAST]]
            l_transaction = [c.layout.get_layout for c in self.__controllers[self._TRANSACTION]]
            l_app = [c.layout.get_layout for c in self.__controllers[self._APP]]
        else:
            l_token_holders = self.__get_token_holder_charts()
            l_vote = self.__get_vote_charts()
            l_cast = self.__get_cast_charts()
            l_transaction = self.__get_transaction_charts()
            l_app = self.__get_app_charts()

        return {
            TEXT['title_section_token_holders']: l_token_holders,
            TEXT['title_section_vote']: l_vote,
            TEXT['title_section_cast']: l_cast,
            TEXT['title_section_transaction']: l_transaction,
            TEXT['title_section_app']: l_app,
        }


    def __get_token_holder_charts(self) -> List[Callable[[], html.Div]]:
        return [lambda: html.Div()]


    def __get_vote_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # new proposal
        charts.append(self.__create_chart(
            title=TEXT['title_new_votations'],
            adapter=BasicAdapter(
                metric_id=s_factory.NEW_VOTES, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        return charts


    def __get_cast_charts(self) -> List[Callable[[], html.Div]]:
        return [lambda: html.Div()]


    def __get_transaction_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # new transactions
        charts.append(self.__create_chart(
            title=TEXT['title_new_transactions'],
            adapter=BasicAdapter(
                metric_id=s_factory.NEW_TRANSACTIONS, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._TRANSACTION
        ))
        return charts


    def __get_app_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # installed apps
        charts.append(self.__create_chart(
            title=TEXT['title_installed_apps'],
            adapter=InstalledApps(organizations=call),
            figure=BarFigure(),
            cont_key=self._APP
        ))
        self.__controllers[self._APP][-1].layout.configuration.disable_subtitles()

        return charts

    def __create_chart(self, title: str, adapter: IMetricAdapter, figure: Figure
    , cont_key: int) -> Callable:
        """
        Creates the chart layout and its controller, and returns a callable
        to get the html representation.
        """
        css_id: str = f"{TEXT['pane_css_prefix']}{ChartPaneLayout.pane_id()}"
        layout: ChartPaneLayout = ChartPaneLayout(
            title=title,
            css_id=css_id,
            figure=figure
        )
        layout.configuration.set_color(color=COLOR.DARK_BLUE)
        layout.configuration.set_css_border(css_border=TEXT['css_pane_border'])

        controller: ChartController = ChartController(
            css_id=css_id,
            layout=layout,
            adapter=adapter)

        self.__controllers[cont_key].append(controller)
        return layout.get_layout
