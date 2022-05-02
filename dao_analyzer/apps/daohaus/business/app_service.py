"""
   Descp: Manage the application logic, and it's used to interconect the
        data_access and presentation layers.

   Created on: 2-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List, Callable
from dash import html
from dao_analyzer.apps.common.presentation.data_point_layout import DataPointLayout

from dao_analyzer.apps.common.presentation.charts.dt_controller import DataTableController
import dao_analyzer.apps.common.presentation.dashboard_view.dashboard_view as view
import dao_analyzer.apps.common.presentation.dashboard_view.controller as view_cont
from dao_analyzer.apps.common.data_access.daos.organization_dao\
    import OrganizationListDao
from dao_analyzer.apps.common.data_access.requesters.cache_requester import CacheRequester
from dao_analyzer.apps.daohaus.business.metric_adapter.asset_values import AssetsValues
from dao_analyzer.apps.daohaus.business.metric_adapter.asset_tokens import AssetsTokens
import dao_analyzer.apps.daohaus.data_access.daos.metric.srcs as srcs
from dao_analyzer.apps.common.business.transfers.organization import OrganizationList
from dao_analyzer.apps.common.presentation.charts.chart_controller import ChartController
from dao_analyzer.apps.common.presentation.charts.chart_sum_controller import ChartSummaryController
from dao_analyzer.apps.common.presentation.charts.layout import ChartPaneLayout, DataTableLayout
from dao_analyzer.apps.common.presentation.charts.layout.figure import Figure, BarFigure, MultiBarFigure, TreemapFigure
from dao_analyzer.apps.common.business.i_metric_adapter import IMetricAdapter
from dao_analyzer.apps.common.business.singleton import Singleton
from dao_analyzer.apps.daohaus.business.metric_adapter.basic_adapter import BasicAdapter
from dao_analyzer.apps.daohaus.business.metric_adapter.votes_type import VotesType
from dao_analyzer.apps.daohaus.business.metric_adapter.proposal_outcome import ProposalOutcome
from dao_analyzer.apps.daohaus.business.metric_adapter.proposal_type import ProposalType 
import dao_analyzer.apps.daohaus.data_access.daos.metric.metric_dao_factory as s_factory
from dao_analyzer.apps.daohaus.resources.strings import TEXT

class DaohausService(metaclass=Singleton):
    _MEMBER: int = 0
    _VOTE: int = 1
    _RAGE_QUIT: int = 2
    _PROPOSAL: int = 3
    _ORGANIZATION: int = 4
    _ASSETS: int = 5

    def __init__(self):
        # app state
        self.__cacheRequester: CacheRequester = CacheRequester(srcs=[srcs.MOLOCHES])
        self.__orgsDAO: OrganizationListDao = OrganizationListDao(self.__cacheRequester)
        self.__controllers: Dict[int, List[ChartController]] = {
            self._MEMBER: list(),
            self._VOTE: list(),
            self._RAGE_QUIT: list(),
            self._PROPOSAL: list(),
            self._ORGANIZATION: list(),
            self._ASSETS: list()
        }
        self.__already_bound: bool = False
        self.__data_points = {}


    def bind_callbacks(self, app) -> None:
        if not self.__already_bound:
            self.__already_bound = True
            view_cont.bind_callbacks(
                app=app,
                section_id=TEXT['css_id_organization'],
                organizationsDAO=self.__orgsDAO
                )
            self.__gen_sections()

            for contList in self.__controllers.values():
                for c in contList:
                    if hasattr(c, 'bind_callback'):
                        c.bind_callback(app)

    def organizations(self) -> OrganizationList:
        return self.__orgsDAO.get_organizations()

    @property
    def are_panes(self) -> bool:
        """
        Checks if panes and their controllers are already created.
        """
        return any(self.__controllers.values())


    def get_layout(self, org_value: str=None) -> html.Div:
        """
        Returns the app's layout. 
        """
        if not self.__already_bound:
            self.bind_callbacks()

        return view.generate_layout(
            labels=self.organizations().get_dict_representation(),
            sections=self.__get_sections(),
            ecosystem='daohaus',
            update=self.__cacheRequester.get_last_update_str(),
            org_id=TEXT['css_id_organization'],
            org_value=org_value,
            datapoints=self.__get_datapoints(),
        )


    def __gen_sections(self) -> None:
        self.__get_member_charts()
        self.__get_vote_charts()
        self.__get_rage_quits_charts()
        self.__get_proposal_charts()
        self.__get_organization_charts()
        self.__get_assets_charts()

    def __get_sections(self) -> Dict[str, List[Callable]]:
        """
        Returns a dict with each section filled with a callable function which
         returns the chart layout
        """
        l_member: List[Callable] = list()
        l_vote: List[Callable] = list()
        l_rage_q: List[Callable] = list()
        l_proposal: List[Callable] = list()
        l_organization: List[Callable] = list()
        l_assets: List[Callable] = list()

        if not self.are_panes:
            self.__gen_sections()

        # Panes are already created.
        l_member = [c.layout.get_layout for c in self.__controllers[self._MEMBER]]
        l_vote = [c.layout.get_layout for c in self.__controllers[self._VOTE]]
        l_rage_q = [c.layout.get_layout for c in self.__controllers[self._RAGE_QUIT]]
        l_proposal = [c.layout.get_layout for c in self.__controllers[self._PROPOSAL]]
        l_organization = [c.layout.get_layout for c in self.__controllers[self._ORGANIZATION]]
        l_assets = [c.layout.get_layout for c in self.__controllers[self._ASSETS]]

        return {
            TEXT['title_activity']: {
                'callables': l_organization,
                'css_id': TEXT['css_id_activity'],
            },
            TEXT['title_member']: {
                'callables': l_member,
                'css_id': TEXT['css_id_member'],
            },
            TEXT['title_rage_quits']: {
                'callables': l_rage_q,
                'css_id': TEXT['css_id_rage_quit'],
            },
            TEXT['title_vote']: {
                'callables': l_vote,
                'css_id': TEXT['css_id_vote'],
            },
            TEXT['title_proposal']: {
                'callables': l_proposal,
                'css_id': TEXT['css_id_proposal'],
            },
            TEXT['title_assets']: {
                'callables': l_assets,
                'css_id': TEXT['css_id_assets']
            }
        }

    def __get_datapoints(self):
        if not self.are_panes:
            self.__gen_sections()

        return self.__data_points

    def __get_organization_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # active organizations
        charts.append(self.__create_chart(
            title=TEXT['title_active_organization'],
            adapter=BasicAdapter(
                metric_id=s_factory.ACTIVE_ORGANIZATION, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._ORGANIZATION
        ))
        return charts



    def __get_member_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # new members
        charts.append(self.__create_chart(
            title=TEXT['title_new_members'],
            adapter=BasicAdapter(
                metric_id=s_factory.NEW_MEMBERS, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._MEMBER
        ))

        # total members
        charts.append(self.__create_sum_chart(
            title=TEXT['title_total_members'],
            adapter=BasicAdapter(
                metric_id=s_factory.TOTAL_MEMBERS, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._MEMBER,
            dp_id=TEXT['dp_id_members'],
            dp_title=TEXT['dp_title_members'],
        ))

        # active members
        charts.append(self.__create_chart(
            title=TEXT['title_active_members'],
            adapter=BasicAdapter(
                metric_id=s_factory.ACTIVE_MEMBERS, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._MEMBER
        ))
        return charts


    def __get_vote_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # votes by type
        charts.append(self.__create_chart(
            title=TEXT['title_vote_type'],
            adapter=VotesType(call),
            figure=MultiBarFigure(bar_type=MultiBarFigure.STACK),
            cont_key=self._VOTE
        ))

        # votes for rate
        charts.append(self.__create_chart(
            title=TEXT['title_vote_for_rate'],
            adapter=BasicAdapter(
                metric_id=s_factory.VOTES_FOR_RATE, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        self.__controllers[self._VOTE][-1].layout.configuration.disable_subtitles()

        # votes against rate
        charts.append(self.__create_chart(
            title=TEXT['title_vote_against_rate'],
            adapter=BasicAdapter(
                metric_id=s_factory.VOTES_AGAINST_RATE, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        self.__controllers[self._VOTE][-1].layout.configuration.disable_subtitles()

        # active voters
        charts.append(self.__create_chart(
            title=TEXT['title_active_voters'],
            adapter=BasicAdapter(
                metric_id=s_factory.ACTIVE_VOTERS, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))

        # percentage of reputation holders which vote
        charts.append(self.__create_chart(
            title=TEXT['title_voters_percentage'],
            adapter=BasicAdapter(s_factory.VOTERS_PERCENTAGE, call),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        self.__controllers[self._VOTE][-1].layout.configuration.disable_subtitles()
        self.__controllers[self._VOTE][-1].layout.figure\
            .configuration.add_y_params(params={'suffix': '%'})

        # votes-voters rate
        charts.append(self.__create_chart(
            title=TEXT['title_votes_voters'],
            adapter=BasicAdapter(
                metric_id=s_factory.VOTES_VOTERS_RATE, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        return charts


    def __get_rage_quits_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # rage quits
        charts.append(self.__create_chart(
            title=TEXT['title_out_members'],
            adapter=BasicAdapter(
                metric_id=s_factory.OUTGOING_MEMBERS, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._RAGE_QUIT
        ))
        return charts


    def __get_proposal_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # new proposals
        charts.append(self.__create_sum_chart(
            title=TEXT['title_new_proposals'],
            adapter=BasicAdapter(
                metric_id=s_factory.NEW_PROPOSALS, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._PROPOSAL,
            dp_id=TEXT['dp_id_proposals'],
            dp_title=TEXT['dp_title_proposals'],
        ))

        # proposal outcomes
        charts.append(self.__create_chart(
            title=TEXT['title_proposal_outcomes'],
            adapter=ProposalOutcome(call),
            figure=MultiBarFigure(bar_type=MultiBarFigure.STACK),
            cont_key=self._PROPOSAL
        ))

        # approval proposal rate
        charts.append(self.__create_chart(
            title=TEXT['title_approval_proposal_rate'],
            adapter=BasicAdapter(
                metric_id=s_factory.APPROVAL_PROPOSAL_RATE, 
                organizations=call),
            figure=BarFigure(),
            cont_key=self._PROPOSAL
        ))
        self.__controllers[self._PROPOSAL][-1].layout.configuration.disable_subtitles()

        # proposal types
        charts.append(self.__create_chart(
            title=TEXT['title_proposal_type'],
            adapter=ProposalType(call),
            figure=MultiBarFigure(bar_type=MultiBarFigure.STACK),
            cont_key=self._PROPOSAL
        ))
        self.__controllers[self._PROPOSAL][-1].layout.configuration.disable_subtitles()
        
        return charts

    
    def __get_assets_charts(self):
        charts: List[Callable] = list()
        call: Callable = self.organizations

        # assets with value
        # TODO: Show value in $ in the title
        charts.append(self.__create_sum_chart(
            title=TEXT['title_assets_value'],
            adapter=AssetsValues(call),
            figure=TreemapFigure(),
            cont_key=self._ASSETS,
            dp_id=TEXT['dp_id_treasury'],
            dp_title=TEXT['dp_title_treasury'],
            dp_hide_evolution=True,
        ))
        self.__controllers[self._ASSETS][-1].layout.configuration.disable_subtitles()

        # assets without value (other tokens)
        charts.append(self.__create_dataTable(
            title=TEXT['title_assets_novalue'],
            adapter=AssetsTokens(call),
            cont_key=self._ASSETS
        ))
 
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

    def __create_sum_chart(self, 
        title: str,
        adapter: IMetricAdapter,
        figure: Figure,
        cont_key: int,
        dp_id: str,
        dp_title: str,
        dp_hide_evolution: bool = False,
    ):
        """
        Creates the chart layout and its summary controller, and returns a callable
        to get the html representation.
        """
        css_id: str = f"{TEXT['pane_css_prefix']}{ChartPaneLayout.pane_id()}"
        layout: ChartPaneLayout = ChartPaneLayout(
            title=title,
            css_id=css_id,
            figure=figure
        )
        layout.configuration.set_css_border(css_border=TEXT['css_pane_border'])

        self.__data_points[dp_id] = DataPointLayout(
            css_id=dp_id,
            title=dp_title,
            hide_evolution=dp_hide_evolution,
        )

        controller: ChartController = ChartSummaryController(
            css_id=css_id,
            layout=layout,
            adapter=adapter,
            datapoint_layout=self.__data_points[dp_id],
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
