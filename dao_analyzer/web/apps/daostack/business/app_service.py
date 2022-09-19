"""
   Descp: Manage the application logic, and it's used to interconect the
        data_access and presentation layers.

   Created on: 2-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List, Callable
from dash import html
import dao_analyzer_components as dac

from dao_analyzer.web.apps.common.business.i_metric_adapter import IMetricAdapter
from dao_analyzer.web.apps.common.business.transfers import Platform, OrganizationList
from dao_analyzer.web.apps.common.presentation.charts.chart_sum_controller import ChartSummaryController
import dao_analyzer.web.apps.common.presentation.dashboard_view.dashboard_view as view
import dao_analyzer.web.apps.common.presentation.dashboard_view.controller as view_cont
from dao_analyzer.web.apps.daostack.data_access.daos.platform_dao import DaostackDAO
from dao_analyzer.web.apps.common.data_access.daos.platform_dao import PlatformDAO
import dao_analyzer.web.apps.daostack.data_access.daos.metric.\
    metric_dao_factory as s_factory
from dao_analyzer.web.apps.common.business.singleton import Singleton
from dao_analyzer.web.apps.common.presentation.charts.chart_controller import ChartController
from dao_analyzer.web.apps.daostack.business.metric_adapter.metric_adapter import MetricAdapter
from dao_analyzer.web.apps.daostack.business.metric_adapter.proposal_boost_outcome \
    import ProposalBoostOutcome
from dao_analyzer.web.apps.daostack.business.metric_adapter.success_ratio_type \
    import SuccessRatioType
from dao_analyzer.web.apps.daostack.business.metric_adapter.vote_type \
    import VoteType
from dao_analyzer.web.apps.daostack.business.metric_adapter.majority_type \
    import MajorityType
from dao_analyzer.web.apps.daostack.business.metric_adapter.asset_tokens import AssetsTokens
from dao_analyzer.web.apps.daostack.business.metric_adapter.asset_values import AssetsValues
from dao_analyzer.web.apps.common.presentation.charts.dt_controller import DataTableController
from dao_analyzer.web.apps.common.presentation.charts.layout import ChartPaneLayout, DataTableLayout
from dao_analyzer.web.apps.common.presentation.charts.layout.figure import BarFigure, CalFigure, MultiBarFigure, DoubleScatterFigure, Figure, TreemapFigure
from dao_analyzer.web.apps.daostack.resources.strings import TEXT

class DaostackService(metaclass=Singleton):
 
    _REP_H: int = 0
    _VOTE: int = 1
    _STAKE: int = 2
    _PROPOSAL: int = 3
    _ORGANIZATION: int = 4
    _ASSETS: int = 5

    def __init__(self):
        # app state
        self.__orgsDAO: PlatformDAO = DaostackDAO()
        self.__controllers: Dict[int, List[ChartController]] = {
            self._REP_H: list(),
            self._VOTE: list(),
            self._STAKE: list(),
            self._PROPOSAL: list(),
            self._ORGANIZATION: list(),
            self._ASSETS: list(),
        }
        self.__already_bound: bool = False
        self.__data_points: Dict[str, dac.DataPoint] = {}


    def bind_callbacks(self, app) -> None:
        if not self.__already_bound:
            self.__already_bound = True
            # Changing the DAO name if it changes
            view_cont.bind_callbacks(
                app=app,
                section_id=TEXT['css_id_organization'],
            )
            self.__gen_sections()

            for contList in self.__controllers.values():
                for c in contList:
                    if hasattr(c, 'bind_callback'):
                        c.bind_callback(app)


    def platform(self, orglist = None) -> Platform:
        return self.__orgsDAO.get_platform(orglist)

    def organization_list(self) -> OrganizationList:
        return self.__orgsDAO.get_organization_list()

    @property
    def are_panes(self) -> bool:
        """
        Checks if panes and their controllers are already created.
        """
        return any(self.__controllers.values())


    # Called every request
    def get_layout(self, **kwargs) -> html.Div:
        """
        Returns the app's layout. 
        """
        if not self.__already_bound:
            self.bind_callbacks()

        org_list = self.organization_list()

        return view.generate_layout(
            organization_list=org_list,
            platform_info=self.platform(org_list),
            sections=self.__get_sections(),
            update=self.__orgsDAO.get_last_update_str(),
            platform_id=TEXT['css_id_organization'],
            datapoints=self.__get_datapoints(),
            **kwargs,
        )

    def __gen_sections(self) -> None:
        self.__get_rep_holder_charts()
        self.__get_vote_charts()
        self.__get_stake_charts()
        self.__get_proposal_charts()
        self.__get_organization_charts()
        self.__get_assets_charts()

    def __get_sections(self) -> Dict[str, List[Callable]]:
        """
        Returns a dict with each section filled with a callable function, which
         returns the chart layout.
        """
        l_rep_h: List[Callable] = list()
        l_vote: List[Callable] = list()
        l_stake: List[Callable] = list()
        l_proposal: List[Callable] = list()
        l_organization: List[Callable] = list()
        l_assets: List[Callable] = list()

        if not self.are_panes:
            self.__gen_sections()

        # Panes are already created.
        l_rep_h = [c.layout.get_layout for c in self.__controllers[self._REP_H]]
        l_vote = [c.layout.get_layout for c in self.__controllers[self._VOTE]]
        l_stake = [c.layout.get_layout for c in self.__controllers[self._STAKE]]
        l_proposal = [c.layout.get_layout for c in self.__controllers[self._PROPOSAL]]
        l_organization = [c.layout.get_layout for c in self.__controllers[self._ORGANIZATION]]
        l_assets = [c.layout.get_layout for c in self.__controllers[self._ASSETS]]

        return {
            TEXT['activity_title'] : {
                'callables': l_organization,
                'css_id': TEXT['css_id_activity'],
                'disclaimer': TEXT['disclaimer_activity'],
            },
            TEXT['rep_holder_title']: {
                'callables': l_rep_h,
                'css_id': TEXT['css_id_reputation_holders'],
            },
            TEXT['proposal_title']: {
                'callables': l_proposal,
                'css_id': TEXT['css_id_proposal'],
            },
            TEXT['vote_title']: {
                'callables': l_vote,
                'css_id': TEXT['css_id_votes'],
            },
            TEXT['stake_title']: {
                'callables': l_stake,
                'css_id': TEXT['css_id_stake'],
            },
            TEXT['assets_title']: {
                'callables': l_assets,
                'css_id': TEXT['css_id_assets'],
            },
        }

    def __get_datapoints(self):
        if not self.are_panes:
            self.__gen_sections()

        return self.__data_points.values()


    def __get_organization_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()

        # active organizations
        charts.append(self.__create_chart(
            title=TEXT['title_active_organization'],
            adapter=MetricAdapter(s_factory.ACTIVE_ORGANIZATION),
            figure=CalFigure(),
            cont_key=self._ORGANIZATION,
            css_classes=['only-on-all-orgs'],
        ))

        charts.append(self.__create_chart(
            title=TEXT['title_organization_activity'],
            adapter=MetricAdapter(s_factory.ORGANIZATION_ACTIVITY),
            figure=CalFigure(),
            cont_key=self._ORGANIZATION
        ))

        return charts


    def __get_rep_holder_charts(self) -> List[Callable[[], html.Div]]:
        """
        Creates charts of reputation holder section, this includes 
         its layout and its controller.
        """
        charts: List[Callable] = list()

        # new reputation holders
        charts.append(self.__create_chart(
            title=TEXT['new_users_title'],
            adapter=MetricAdapter(s_factory.NEW_USERS),
            figure=BarFigure(),
            cont_key=self._REP_H
        ))

        # total reputation holders
        charts.append(self.__create_sum_chart(
            title=TEXT['total_users_title'],
            adapter=MetricAdapter(s_factory.TOTAL_REP_HOLDERS),
            figure=BarFigure(),
            cont_key=self._REP_H,
            dp_id=TEXT['total_users_dp_id'],
            dp_title=TEXT['total_users_dp_title'],
        ))

        # active reputation holders
        charts.append(self.__create_sum_chart(
            title=TEXT['active_users_title'],
            adapter=MetricAdapter(s_factory.ACTIVE_USERS),
            figure=BarFigure(),
            cont_key=self._REP_H,
            dp_id=TEXT['active_users_dp_id'],
            dp_title=TEXT['active_users_dp_title'],
        ))
        return charts


    def __get_vote_charts(self) -> List[Callable[[], html.Div]]:
        """
        Creates charts of vote section.
        """
        charts: List[Callable] = list()

        # total votes by type
        charts.append(self.__create_chart(
            title=TEXT['total_votes_option_title'],
            adapter=VoteType(s_factory.TOTAL_VOTES_OPTION, VoteType.VOTE),
            figure=MultiBarFigure(bar_type=MultiBarFigure.STACK),
            cont_key=self._VOTE
        ))

        # votes for rate
        charts.append(self.__create_chart(
            title=TEXT['vote_for_rate_title'],
            adapter=MetricAdapter(s_factory.VOTES_FOR_RATE),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        self.__controllers[self._VOTE][-1].layout.configuration.disable_subtitles()

        # votes against rate
        charts.append(self.__create_chart(
            title=TEXT['vote_against_rate_title'],
            adapter=MetricAdapter(s_factory.VOTES_AGAINST_RATE),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        self.__controllers[self._VOTE][-1].layout.configuration.disable_subtitles()

        # different voters
        charts.append(self.__create_chart(
            title=TEXT['different_voters_title'],
            adapter=MetricAdapter(s_factory.DIFFERENT_VOTERS),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))

        # percentage of reputation holders which vote
        charts.append(self.__create_chart(
            title=TEXT['voters_percentage_title'],
            adapter=MetricAdapter(s_factory.VOTERS_PERCENTAGE),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        self.__controllers[self._VOTE][-1].layout.configuration.disable_subtitles()
        self.__controllers[self._VOTE][-1].layout.figure\
            .configuration.add_y_params(params={
                'suffix': '%'})

        # vote-voters rate
        charts.append(self.__create_chart(
            title=TEXT['vote_voters_title'],
            adapter=MetricAdapter(s_factory.VOTE_VOTERS_RATE),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))

        return charts


    def __get_stake_charts(self) -> List[Callable[[], html.Div]]:
        """
        Creates charts of stake section.
        """
        charts: List[Callable] = list()

        # total stakes
        charts.append(self.__create_chart(
            title=TEXT['total_stakes_title'],
            adapter=MetricAdapter(s_factory.TOTAL_STAKES),
            figure=BarFigure(),
            cont_key=self._STAKE
        ))
        # different stakers
        charts.append(self.__create_chart(
            title=TEXT['different_stakers_title'],
            adapter=MetricAdapter(s_factory.DIFFERENT_STAKERS),
            figure=BarFigure(),
            cont_key=self._STAKE
        ))
        return charts


    def __get_proposal_charts(self) -> List[Callable[[], html.Div]]:
        """
        Creates charts of proposal section.
        """
        charts: List[Callable] = list()

        # new proposals
        charts.append(self.__create_sum_chart(
            title=TEXT['new_proposals_title'],
            adapter=MetricAdapter(s_factory.NEW_PROPOSALS),
            figure=BarFigure(),
            cont_key=self._PROPOSAL,
            dp_id=TEXT['new_proposals_dp_id'],
            dp_title=TEXT['new_proposals_dp_title'],
        ))

        # majority type
        charts.append(self.__create_chart(
            title=TEXT['proposal_outcome_majority_title'],
            adapter=MajorityType(s_factory.PROPOSAL_MAJORITY),
            figure=DoubleScatterFigure(),
            cont_key=self._PROPOSAL
        ))
        self.__controllers[self._PROPOSAL][-1].layout.configuration.disable_subtitles()

        # proposal boost_outcome
        charts.append(self.__create_chart(
            title=TEXT['proposal_boost_outcome_title'],
            adapter=ProposalBoostOutcome(s_factory.PROPOSALS_BOOST_OUTCOME),
            figure=MultiBarFigure(bar_type=MultiBarFigure.STACK),
            cont_key=self._PROPOSAL
        ))
        self.__controllers[self._PROPOSAL][-1].layout.configuration.disable_subtitles()

        # proposal approve rate
        charts.append(self.__create_chart(
            title=TEXT['approval_proposal_rate_title'],
            adapter=MetricAdapter(s_factory.APPROVAL_PROPOSAL_RATE),
            figure=BarFigure(),
            cont_key=self._PROPOSAL
        ))
        self.__controllers[self._PROPOSAL][-1].layout.configuration.disable_subtitles()

        # total succes rate of the stakes
        charts.append(self.__create_chart(
            title=TEXT['proposal_total_succ_rate_title'],
            adapter=MetricAdapter(s_factory.PROPOSALS_TOTAL_SUCCES_RATIO),
            figure=BarFigure(),
            cont_key=self._PROPOSAL
        ))
        self.__controllers[self._PROPOSAL][-1].layout.configuration.disable_subtitles()

        # success rate by type
        charts.append(self.__create_chart(
            title=TEXT['proposal_boost_succ_rate_title'],
            adapter=SuccessRatioType(s_factory.PROPOSALS_BOOST_SUCCES_RATIO),
            figure=MultiBarFigure(bar_type=MultiBarFigure.GROUP),
            cont_key=self._PROPOSAL
        ))
        self.__controllers[self._PROPOSAL][-1].layout.configuration.disable_subtitles()

        return charts

    def __get_assets_charts(self):
        charts: List[Callable] = list()

        charts.append(self.__create_sum_chart(
            title=TEXT['assets_value_title'],
            adapter=AssetsValues(),
            figure=TreemapFigure(),
            cont_key=self._ASSETS,
            dp_id=TEXT['assets_value_dp_id'],
            dp_title=TEXT['assets_value_dp_title'],
        ))
        self.__controllers[self._ASSETS][-1].layout.configuration.disable_subtitles()

        charts.append(self.__create_dataTable(
            title=TEXT['assets_novalue_title'],
            adapter=AssetsTokens(),
            cont_key=self._ASSETS
        ))

        return charts

    def __create_chart(self, title: str, adapter: MetricAdapter, figure: Figure
    , cont_key: int, css_classes = []) -> Callable:
        """
        Creates the chart layout and its controller, and returns a callable
        to get the html representation.
        """
        css_id: str = f"{TEXT['pane_css_prefix']}{ChartPaneLayout.pane_id()}"
        layout: ChartPaneLayout = ChartPaneLayout(
            title=title,
            css_id=css_id,
            figure=figure,
            css_classes=css_classes,
        )
        layout.configuration.set_css_border(css_border=TEXT['css_pane_border'])

        controller: ChartController = ChartController(
            css_id=css_id,
            layout=layout,
            adapter=adapter)

        self.__controllers[cont_key].append(controller)
        return layout.get_layout

    def __create_sum_chart(self,
        title: str, 
        adapter: MetricAdapter, 
        figure: Figure, 
        cont_key: int,
        dp_id: str,
        dp_title: str,
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
        layout.configuration.set_css_border(css_border=TEXT['css_pane_border'])

        self.__data_points[dp_id] = dac.DataPoint(
            id=dp_id,
            title=dp_title,
        )

        controller: ChartController = ChartSummaryController(
            css_id=css_id,
            layout=layout,
            adapter=adapter,
            dp_id=dp_id,
        )

        self.__controllers[cont_key].append(controller)
        return layout.get_layout
    
    def __create_dataTable(self, title: str, adapter: IMetricAdapter, cont_key: int) -> Callable:
        """Creates a datatable to put alongside charts
        Args:
            title (str): The title of the datatable
            adapter (IMetricAdapter): The adapter to get the data from
            cont_key (int): The key of the controller
        Returns:
            Callable: Layout html builder
        """
        css_id: str = f"{TEXT['pane_css_prefix']}{ChartPaneLayout.pane_id()}"

        layout: DataTableLayout = DataTableLayout(
            title=title,
            css_id=css_id
        )

        controller: DataTableController = DataTableController(
            table_id=layout.table_id,
            layout=layout,
            adapter=adapter
        )

        self.__controllers[cont_key].append(controller)
        return layout.get_layout
