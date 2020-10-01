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
# from src.apps.common.presentation.charts.layout.chart_pane_layout \
#     import ChartPaneLayout
# from src.apps.common.presentation.charts.layout.figure.figure import Figure
from src.apps.daohaus.resources.strings import TEXT


__service = None

def get_service():
    """
    Singelton object.
    """
    global __service
    if not __service:
        __service = Service()
    return __service


class Service():
 
    def __init__(self):
        # app state
        self.__orgs: OrganizationList = None
        self.__controllers: List[ChartController] = list()


    @property
    def organizations(self) -> OrganizationList:
        if not self.__orgs:
            orgs: OrganizationList = OrganizationListDao(cache.CacheRequester(
                srcs=[cache.MOLOCHES])).get_organizations()
            if not orgs.is_empty():
                self.__orgs = orgs
                
        return self.__orgs


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
        return {
            TEXT['title_member']: self.__get_member_charts(),
            TEXT['title_vote']: self.__get_vote_charts(),
            TEXT['title_rage_quits']: self.__get_rage_quits_charts(),
            TEXT['title_proposal']: self.__get_proposal_charts(),
        }


    def __get_member_charts(self) -> List[Callable[[], html.Div]]:
        return [lambda: html.Div()]


    def __get_vote_charts(self) -> List[Callable[[], html.Div]]:
        return [lambda: html.Div()]


    def __get_rage_quits_charts(self) -> List[Callable[[], html.Div]]:
        return [lambda: html.Div()]


    def __get_proposal_charts(self) -> List[Callable[[], html.Div]]:
        return [lambda: html.Div()]


    # def __create_chart(self, title: str, adapter: MetricAdapter, figure: Figure
    # ) -> Callable:
    #     """
    #     Creates the chart layout and its controller, and returns a callable
    #     to get the html representation.
    #     """
    #     css_id: str = f"{TEXT['pane_css_prefix']}{ChartPaneLayout.pane_id()}"
    #     layout: ChartPaneLayout = ChartPaneLayout(
    #         title=title,
    #         css_id=css_id,
    #         figure=figure
    #     )

    #     controller: ChartController = ChartController(
    #         css_id=css_id,
    #         layout=layout,
    #         adapter=adapter)

    #     self.__controllers.append(controller)
    #     return layout.get_layout
