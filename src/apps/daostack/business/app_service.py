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
import src.apps.daostack.data_access.daos.metric.\
    metric_dao_factory as s_factory
import src.apps.daostack.data_access.requesters.cache_requester as cache
from src.apps.common.business.transfers.organization import OrganizationList
from src.apps.common.presentation.charts.chart_controller import ChartController
from src.apps.daostack.business.metric_adapter.metric_adapter import MetricAdapter
from src.apps.daostack.business.metric_adapter.proposal_boost_outcome \
    import ProposalBoostOutcome
from src.apps.daostack.business.metric_adapter.success_ratio_type \
    import SuccessRatioType
from src.apps.daostack.business.metric_adapter.vote_type \
    import VoteType
from src.apps.daostack.business.metric_adapter.majority_type \
    import MajorityType
from src.apps.common.presentation.charts.layout.chart_pane_layout \
    import ChartPaneLayout
from src.apps.common.presentation.charts.layout.figure.bar_figure import BarFigure
from src.apps.common.presentation.charts.layout.figure.multi_bar_figure \
    import MultiBarFigure
from src.apps.common.presentation.charts.layout.figure.double_scatter_figure \
    import DoubleScatterFigure
from src.apps.common.presentation.charts.layout.figure.figure import Figure
from src.apps.daostack.resources.strings import TEXT


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
                srcs=[cache.DAOS])).get_organizations()
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
            TEXT['rep_holder_title']: self.__get_rep_holder_charts(),
            TEXT['vote_title']: self.__get_vote_charts(),
            TEXT['stake_title']: self.__get_stake_charts(),
            TEXT['proposal_title']: self.__get_proposal_charts(),
        }


    def __get_rep_holder_charts(self) -> List[Callable[[], html.Div]]:
        """
        Creates charts of reputation holder section, this includes 
         its layout and its controller.
        """
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # new reputation holders
        charts.append(self.__create_chart(
            title=TEXT['new_users_title'],
            adapter=MetricAdapter(s_factory.NEW_USERS, call),
            figure=BarFigure()
        ))
        # active reputation holders
        charts.append(self.__create_chart(
            title=TEXT['active_users_title'],
            adapter=MetricAdapter(s_factory.ACTIVE_USERS, call),
            figure=BarFigure()
        ))
        return charts


    def __get_vote_charts(self) -> List[Callable[[], html.Div]]:
        """
        Creates charts of vote section.
        """
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # total votes by type
        charts.append(self.__create_chart(
            title=TEXT['total_votes_option_title'],
            adapter=VoteType(s_factory.TOTAL_VOTES_OPTION, call, VoteType.VOTE),
            figure=MultiBarFigure(bar_type=MultiBarFigure.STACK)
        ))

        # different voters
        charts.append(self.__create_chart(
            title=TEXT['different_voters_title'],
            adapter=MetricAdapter(s_factory.DIFFERENT_VOTERS, call),
            figure=BarFigure()
        ))
        return charts


    def __get_stake_charts(self) -> List[Callable[[], html.Div]]:
        """
        Creates charts of stake section.
        """
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # total stakes
        charts.append(self.__create_chart(
            title=TEXT['total_stakes_title'],
            adapter=MetricAdapter(s_factory.TOTAL_STAKES, call),
            figure=BarFigure()
        ))
        # different stakers
        charts.append(self.__create_chart(
            title=TEXT['different_stakers_title'],
            adapter=MetricAdapter(s_factory.DIFFERENT_STAKERS, call),
            figure=BarFigure()
        ))
        return charts


    def __get_proposal_charts(self) -> List[Callable[[], html.Div]]:
        """
        Creates charts of proposal section.
        """
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # new proposals
        charts.append(self.__create_chart(
            title=TEXT['new_proposals_title'],
            adapter=MetricAdapter(s_factory.NEW_PROPOSALS, call),
            figure=BarFigure()
        ))

        # majority type
        charts.append(self.__create_chart(
            title=TEXT['proposal_outcome_majority_title'],
            adapter=MajorityType(s_factory.PROPOSAL_MAJORITY, call),
            figure=DoubleScatterFigure()
        ))
        self.__controllers[-1].layout.configuration.disable_subtitles()

        # proposal boost_outcome
        charts.append(self.__create_chart(
            title=TEXT['proposal_boost_outcome_title'],
            adapter=ProposalBoostOutcome(s_factory.PROPOSALS_BOOST_OUTCOME, call),
            figure=MultiBarFigure(bar_type=MultiBarFigure.STACK)
        ))
        self.__controllers[-1].layout.configuration.disable_subtitles()

        # total succes rate of the stakes
        charts.append(self.__create_chart(
            title=TEXT['proposal_total_succ_rate_title'],
            adapter=MetricAdapter(s_factory.PROPOSALS_TOTAL_SUCCES_RATIO, call),
            figure=BarFigure()
        ))
        self.__controllers[-1].layout.configuration.disable_subtitles()

        # success rate by type
        charts.append(self.__create_chart(
            title=TEXT['proposal_boost_succ_rate_title'],
            adapter=SuccessRatioType(s_factory.PROPOSALS_BOOST_SUCCES_RATIO, call),
            figure=MultiBarFigure(bar_type=MultiBarFigure.GROUP)
        ))
        self.__controllers[-1].layout.configuration.disable_subtitles()

        return charts


    def __create_chart(self, title: str, adapter: MetricAdapter, figure: Figure
    ) -> Callable:
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

        self.__controllers.append(controller)
        return layout.get_layout
