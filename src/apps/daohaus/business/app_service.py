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
import src.apps.daohaus.data_access.requesters.cache_requester as cache
from src.apps.common.business.transfers.organization import OrganizationList
from src.apps.common.presentation.charts.chart_controller import ChartController
from src.apps.common.presentation.charts.layout.chart_pane_layout \
    import ChartPaneLayout
from src.apps.common.presentation.charts.layout.figure.figure import Figure
from src.apps.common.presentation.charts.layout.figure.bar_figure import BarFigure
from src.apps.common.business.i_metric_adapter import IMetricAdapter
from src.apps.daohaus.business.metric_adapter.new_members import NewMembers
#import src.apps.daohaus.data_access.daos.metric.metric_dao_factory as s_factory
from src.apps.daohaus.resources.strings import TEXT


_daohaus_service = None

def get_service():
    """
    Singelton object.
    """
    global _daohaus_service

    if not _daohaus_service:
        _daohaus_service = DaohausService()

    return _daohaus_service


class DaohausService():
    _MEMBER: int = 0
    _VOTE: int = 1
    _RAGE_QUIT: int = 2
    _PROPOSAL: int = 3

    def __init__(self):
        # app state
        self.__orgs: OrganizationList = None
        self.__controllers: Dict[int, List[ChartController]] = {
            self._MEMBER: list(),
            self._VOTE: list(),
            self._RAGE_QUIT: list(),
            self._PROPOSAL: list(),
        }


    @property
    def organizations(self) -> OrganizationList:
        if not self.__orgs:
            orgs: OrganizationList = OrganizationListDao(cache.CacheRequester(
                srcs=[cache.MOLOCHES])).get_organizations()
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
            sections=self.__get_sections()
        )


    def __get_sections(self) -> Dict[str, List[Callable]]:
        """
        Returns a dict with each section filled with a callable function which
         returns the chart layout
        """
        l_member: List[Callable] = list()
        l_vote: List[Callable] = list()
        l_rage_q: List[Callable] = list()
        l_proposal: List[Callable] = list()

        # Panes are already created.
        if self.are_panes:
            l_member = [c.layout.get_layout for c in self.__controllers[self._MEMBER]]
            l_vote = [c.layout.get_layout for c in self.__controllers[self._VOTE]]
            l_rage_q = [c.layout.get_layout for c in self.__controllers[self._RAGE_QUIT]]
            l_proposal = [c.layout.get_layout for c in self.__controllers[self._PROPOSAL]]
        else:
            l_member = self.__get_member_charts()
            l_vote = self.__get_vote_charts()
            l_rage_q = self.__get_rage_quits_charts()
            l_proposal = self.__get_proposal_charts()

        return {
            TEXT['title_member']: l_member,
            TEXT['title_vote']: l_vote,
            TEXT['title_rage_quits']: l_rage_q,
            TEXT['title_proposal']: l_proposal,
        }


    def __get_member_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # new members
        charts.append(self.__create_chart(
            title=TEXT['title_new_members'],
            adapter=NewMembers(call),
            figure=BarFigure(),
            cont_key=self._MEMBER
        ))
        return charts


    def __get_vote_charts(self) -> List[Callable[[], html.Div]]:
        return [lambda: html.Div()]


    def __get_rage_quits_charts(self) -> List[Callable[[], html.Div]]:
        return [lambda: html.Div()]


    def __get_proposal_charts(self) -> List[Callable[[], html.Div]]:
        return [lambda: html.Div()]


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

        controller: ChartController = ChartController(
            css_id=css_id,
            layout=layout,
            adapter=adapter)

        self.__controllers[cont_key].append(controller)
        return layout.get_layout
