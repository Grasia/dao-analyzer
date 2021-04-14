"""
   Descp: Manage the application logic, and it's used to interconect the
        data_access and presentation layers.

   Created on: 2-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List, Callable
import dash_html_components as html

from src.app import app
from src.apps.common.data_access.update_date import UpdateDate
import src.apps.common.presentation.dashboard_view.dashboard_view as view
import src.apps.common.presentation.dashboard_view.controller as view_cont
from src.apps.common.data_access.daos.organization_dao\
    import OrganizationListDao
import src.apps.aragon.data_access.requesters.cache_requester as cache
from src.apps.common.business.transfers.organization import OrganizationList
from src.apps.common.presentation.charts.chart_controller import ChartController
from src.apps.common.presentation.charts.layout.chart_pane_layout \
    import ChartPaneLayout
from src.apps.common.presentation.charts.layout.figure.figure import Figure
from src.apps.common.presentation.charts.layout.figure.bar_figure import BarFigure
from src.apps.common.presentation.charts.layout.figure.multi_bar_figure import MultiBarFigure
import src.apps.aragon.data_access.daos.metric.metric_dao_factory as s_factory
from src.apps.common.business.i_metric_adapter import IMetricAdapter
from src.apps.aragon.business.metric_adapter.basic_adapter import BasicAdapter
from src.apps.aragon.business.metric_adapter.installed_apps import InstalledApps
from src.apps.aragon.business.metric_adapter.cast_type import CastType
from src.apps.aragon.business.metric_adapter.vote_outcome import VoteOutcome

from src.apps.aragon.resources.strings import TEXT
from src.apps.common.resources.strings import TEXT as COMMON_TEXT


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
    _ORGANIZATION: int = 5

    def __init__(self):
        # app state
        self.__orgs: OrganizationList = None
        self.__controllers: Dict[int, List[ChartController]] = {
            self._TOKEN_HOLDER: list(),
            self._VOTE: list(),
            self._CAST: list(),
            self._TRANSACTION: list(),
            self._APP: list(),
            self._ORGANIZATION: list(),
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
        
        if not self.are_panes:
            view_cont.bind_callbacks(
                app=app, 
                section_id=TEXT['css_id_organization'])
        
        return view.generate_layout(
            labels=orgs.get_dict_representation(),
            sections=self.__get_sections(),
            ecosystem='aragon',
            update=UpdateDate().get_date()
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
        l_organization: List[Callable] = list()

        # Panes are already created.
        if self.are_panes:
            l_token_holders = [c.layout.get_layout for c in self.__controllers[self._TOKEN_HOLDER]]
            l_vote = [c.layout.get_layout for c in self.__controllers[self._VOTE]]
            l_cast = [c.layout.get_layout for c in self.__controllers[self._CAST]]
            l_transaction = [c.layout.get_layout for c in self.__controllers[self._TRANSACTION]]
            l_app = [c.layout.get_layout for c in self.__controllers[self._APP]]
            l_organization = [c.layout.get_layout for c in self.__controllers[self._ORGANIZATION]]
        else:
            l_token_holders = self.__get_token_holder_charts()
            l_vote = self.__get_vote_charts()
            l_cast = self.__get_cast_charts()
            l_transaction = self.__get_transaction_charts()
            l_app = self.__get_app_charts()
            l_organization = self.__get_organization_charts()

        return {
            COMMON_TEXT['no_data_selected']: {
                'callables': l_organization,
                'css_id': TEXT['css_id_organization'],
            },
            TEXT['title_section_token_holders']: {
                'callables': l_token_holders,
                'css_id': TEXT['css_id_token_holder'],
            },
            TEXT['title_section_vote']: {
                'callables': l_vote,
                'css_id': TEXT['css_id_vote'],
            },
            TEXT['title_section_cast']: {
                'callables': l_cast,
                'css_id': TEXT['css_id_cast']
            },
            TEXT['title_section_transaction']: {
                'callables': l_transaction,
                'css_id': TEXT['css_id_transactions'],
            },
            TEXT['title_section_app']: {
                'callables': l_app,
                'css_id': TEXT['css_id_app'],
            },
        }


    def __get_organization_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # active organization
        charts.append(self.__create_chart(
            title=TEXT['title_active_organization'],
            adapter=BasicAdapter(
                metric_id=s_factory.ACTIVE_ORGANIZATION, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._ORGANIZATION
        ))

        return charts


    def __get_token_holder_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # active token holders
        charts.append(self.__create_chart(
            title=TEXT['title_active_token_holders'],
            adapter=BasicAdapter(
                metric_id=s_factory.ACTIVE_TOKEN_HOLDERS, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._TOKEN_HOLDER
        ))

        return charts


    def __get_vote_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # new votes
        charts.append(self.__create_chart(
            title=TEXT['title_new_votes'],
            adapter=BasicAdapter(
                metric_id=s_factory.NEW_VOTES, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))

        # vote's outcome
        charts.append(self.__create_chart(
            title=TEXT['title_vote_outcome'],
            adapter=VoteOutcome(organizations=call),
            figure=MultiBarFigure(MultiBarFigure.STACK),
            cont_key=self._VOTE
        ))

        # approval vote rate
        charts.append(self.__create_chart(
            title=TEXT['title_rate_vote_rate'],
            adapter=BasicAdapter(
                metric_id=s_factory.APPROVAL_VOTE_RATE, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        self.__controllers[self._VOTE][-1].layout.configuration.disable_subtitles()

        return charts


    def __get_cast_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # cast type
        charts.append(self.__create_chart(
            title=TEXT['title_cast_type'],
            adapter=CastType(organizations=call),
            figure=MultiBarFigure(bar_type=MultiBarFigure.STACK),
            cont_key=self._CAST
        ))

        # casted votes for rate
        charts.append(self.__create_chart(
            title=TEXT['title_casted_votes_for_rate'],
            adapter=BasicAdapter(
                metric_id=s_factory.CASTED_VOTE_FOR_RATE,
                organizations=call),
            figure=BarFigure(),
            cont_key=self._CAST
        ))
        self.__controllers[self._CAST][-1].layout.configuration.disable_subtitles()

        # casted votes against rate
        charts.append(self.__create_chart(
            title=TEXT['title_casted_votes_against_rate'],
            adapter=BasicAdapter(
                metric_id=s_factory.CASTED_VOTE_AGAINST_RATE,
                organizations=call),
            figure=BarFigure(),
            cont_key=self._CAST
        ))
        self.__controllers[self._CAST][-1].layout.configuration.disable_subtitles()

        # active voters
        charts.append(self.__create_chart(
            title=TEXT['title_active_voters'],
            adapter=BasicAdapter(
                metric_id=s_factory.ACTIVE_VOTERS,
                organizations=call),
            figure=BarFigure(),
            cont_key=self._CAST
        ))

        # casted votes-voters rate
        charts.append(self.__create_chart(
            title=TEXT['title_votes_voters'],
            adapter=BasicAdapter(
                metric_id=s_factory.CASTED_VOTE_VOTER_RATE,
                organizations=call),
            figure=BarFigure(),
            cont_key=self._CAST
        ))

        return charts


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
        layout.configuration.set_css_border(css_border=TEXT['css_pane_border'])

        controller: ChartController = ChartController(
            css_id=css_id,
            layout=layout,
            adapter=adapter)

        self.__controllers[cont_key].append(controller)
        return layout.get_layout
