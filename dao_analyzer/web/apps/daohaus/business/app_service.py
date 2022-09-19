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

from dao_analyzer.web.apps.common.business.transfers.organization import Platform, OrganizationList

from dao_analyzer.web.apps.common.presentation.charts.dt_controller import DataTableController
import dao_analyzer.web.apps.common.presentation.dashboard_view.dashboard_view as view
import dao_analyzer.web.apps.common.presentation.dashboard_view.controller as view_cont
from dao_analyzer.web.apps.common.data_access.daos.platform_dao\
    import PlatformDAO
from dao_analyzer.web.apps.daohaus.business.metric_adapter.asset_values import AssetsValues
from dao_analyzer.web.apps.daohaus.business.metric_adapter.asset_tokens import AssetsTokens
from dao_analyzer.web.apps.common.presentation.charts.chart_controller import ChartController
from dao_analyzer.web.apps.common.presentation.charts.chart_sum_controller import ChartSummaryController
from dao_analyzer.web.apps.common.presentation.charts.layout import ChartPaneLayout, DataTableLayout
from dao_analyzer.web.apps.common.presentation.charts.layout.figure import Figure, BarFigure, CalFigure, MultiBarFigure, TreemapFigure
from dao_analyzer.web.apps.common.business.i_metric_adapter import IMetricAdapter
from dao_analyzer.web.apps.common.business.singleton import Singleton
from dao_analyzer.web.apps.daohaus.business.metric_adapter.basic_adapter import BasicAdapter
from dao_analyzer.web.apps.daohaus.business.metric_adapter.votes_type import VotesType
from dao_analyzer.web.apps.daohaus.business.metric_adapter.proposal_outcome import ProposalOutcome
from dao_analyzer.web.apps.daohaus.business.metric_adapter.proposal_type import ProposalType 
import dao_analyzer.web.apps.daohaus.data_access.daos.metric.metric_dao_factory as s_factory
from dao_analyzer.web.apps.daohaus.data_access.daos.platform_dao import DaohausDao
from dao_analyzer.web.apps.daohaus.resources.strings import TEXT

class DaohausService(metaclass=Singleton):
    _MEMBER: int = 0
    _VOTE: int = 1
    _PROPOSAL: int = 3
    _ORGANIZATION: int = 4
    _ASSETS: int = 5

    def __init__(self):
        # app state
        self.__orgsDAO: PlatformDAO = DaohausDao()
        self.__controllers: Dict[int, List[ChartController]] = {
            self._MEMBER: list(),
            self._VOTE: list(),
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
                )
            self.__gen_sections()

            for contList in self.__controllers.values():
                for c in contList:
                    if hasattr(c, 'bind_callback'):
                        c.bind_callback(app)

    def platform(self, orglist: OrganizationList) -> Platform:
        return self.__orgsDAO.get_platform(orglist)

    def organization_list(self) -> OrganizationList:
        return self.__orgsDAO.get_organization_list()

    @property
    def are_panes(self) -> bool:
        """
        Checks if panes and their controllers are already created.
        """
        return any(self.__controllers.values())


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
        self.__get_member_charts()
        self.__get_vote_charts()
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
        l_proposal: List[Callable] = list()
        l_organization: List[Callable] = list()
        l_assets: List[Callable] = list()

        if not self.are_panes:
            self.__gen_sections()

        # Panes are already created.
        l_member = [c.layout.get_layout for c in self.__controllers[self._MEMBER]]
        l_vote = [c.layout.get_layout for c in self.__controllers[self._VOTE]]
        l_proposal = [c.layout.get_layout for c in self.__controllers[self._PROPOSAL]]
        l_organization = [c.layout.get_layout for c in self.__controllers[self._ORGANIZATION]]
        l_assets = [c.layout.get_layout for c in self.__controllers[self._ASSETS]]

        return {
            TEXT['title_activity']: {
                'callables': l_organization,
                'css_id': TEXT['css_id_activity'],
                'disclaimer': TEXT['disclaimer_activity']
            },
            TEXT['title_member']: {
                'callables': l_member,
                'css_id': TEXT['css_id_member'],
            },
            TEXT['title_proposal']: {
                'callables': l_proposal,
                'css_id': TEXT['css_id_proposal'],
            },
            TEXT['title_vote']: {
                'callables': l_vote,
                'css_id': TEXT['css_id_vote'],
            },
            TEXT['title_assets']: {
                'callables': l_assets,
                'css_id': TEXT['css_id_assets']
            }
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
            adapter=BasicAdapter(
                metric_id=s_factory.ACTIVE_ORGANIZATION, 
            ),
            figure=CalFigure(),
            cont_key=self._ORGANIZATION,
            css_classes=['only-on-all-orgs']
        ))
        
        charts.append(self.__create_chart(
            title=TEXT['title_organization_activity'],
            adapter=BasicAdapter(
                metric_id=s_factory.ORGANIZATION_ACTIVITY,
            ),
            figure=CalFigure(),
            cont_key=self._ORGANIZATION
        ))
        
        return charts



    def __get_member_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()

        # new members
        charts.append(self.__create_chart(
            title=TEXT['title_new_members'],
            adapter=BasicAdapter(
                metric_id=s_factory.NEW_MEMBERS, 
            ),
            figure=BarFigure(),
            cont_key=self._MEMBER
        ))

        # rage quits
        charts.append(self.__create_chart(
            title=TEXT['title_out_members'],
            adapter=BasicAdapter(
                metric_id=s_factory.OUTGOING_MEMBERS, 
            ),
            figure=BarFigure(),
            cont_key=self._MEMBER
        ))

        # total members
        charts.append(self.__create_sum_chart(
            title=TEXT['title_total_members'],
            adapter=BasicAdapter(
                metric_id=s_factory.TOTAL_MEMBERS, 
            ),
            figure=BarFigure(),
            cont_key=self._MEMBER,
            dp_id=TEXT['dp_id_members'],
            dp_title=TEXT['dp_title_members'],
        ))

        # active members
        charts.append(self.__create_sum_chart(
            title=TEXT['title_active_members'],
            adapter=BasicAdapter(
                metric_id=s_factory.ACTIVE_MEMBERS, 
            ),
            figure=BarFigure(),
            cont_key=self._MEMBER,
            dp_id=TEXT['dp_id_active_members'],
            dp_title=TEXT['dp_title_active_members'],
        ))

        return charts


    def __get_vote_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()

        # votes by type
        charts.append(self.__create_chart(
            title=TEXT['title_vote_type'],
            adapter=VotesType(),
            figure=MultiBarFigure(bar_type=MultiBarFigure.STACK),
            cont_key=self._VOTE
        ))

        # votes for rate
        charts.append(self.__create_chart(
            title=TEXT['title_vote_for_rate'],
            adapter=BasicAdapter(
                metric_id=s_factory.VOTES_FOR_RATE, 
            ),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        self.__controllers[self._VOTE][-1].layout.configuration.disable_subtitles()

        # votes against rate
        charts.append(self.__create_chart(
            title=TEXT['title_vote_against_rate'],
            adapter=BasicAdapter(
                metric_id=s_factory.VOTES_AGAINST_RATE, 
            ),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        self.__controllers[self._VOTE][-1].layout.configuration.disable_subtitles()

        # active voters
        charts.append(self.__create_chart(
            title=TEXT['title_active_voters'],
            adapter=BasicAdapter(
                metric_id=s_factory.ACTIVE_VOTERS, 
            ),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))

        # percentage of reputation holders which vote
        charts.append(self.__create_chart(
            title=TEXT['title_voters_percentage'],
            adapter=BasicAdapter(s_factory.VOTERS_PERCENTAGE),
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
            ),
            figure=BarFigure(),
            cont_key=self._VOTE
        ))
        return charts


    def __get_proposal_charts(self) -> List[Callable[[], html.Div]]:
        charts: List[Callable] = list()

        # new proposals
        charts.append(self.__create_sum_chart(
            title=TEXT['title_new_proposals'],
            adapter=BasicAdapter(
                metric_id=s_factory.NEW_PROPOSALS, 
            ),
            figure=BarFigure(),
            cont_key=self._PROPOSAL,
            dp_id=TEXT['dp_id_proposals'],
            dp_title=TEXT['dp_title_proposals'],
        ))

        # proposal outcomes
        charts.append(self.__create_chart(
            title=TEXT['title_proposal_outcomes'],
            adapter=ProposalOutcome(),
            figure=MultiBarFigure(bar_type=MultiBarFigure.STACK),
            cont_key=self._PROPOSAL
        ))

        # approval proposal rate
        charts.append(self.__create_chart(
            title=TEXT['title_approval_proposal_rate'],
            adapter=BasicAdapter(
                metric_id=s_factory.APPROVAL_PROPOSAL_RATE, 
            ),
            figure=BarFigure(),
            cont_key=self._PROPOSAL
        ))
        self.__controllers[self._PROPOSAL][-1].layout.configuration.disable_subtitles()

        # proposal types
        charts.append(self.__create_chart(
            title=TEXT['title_proposal_type'],
            adapter=ProposalType(),
            figure=MultiBarFigure(bar_type=MultiBarFigure.STACK),
            cont_key=self._PROPOSAL
        ))
        self.__controllers[self._PROPOSAL][-1].layout.configuration.disable_subtitles()
        
        return charts

    
    def __get_assets_charts(self):
        charts: List[Callable] = list()

        # assets with value
        # TODO: Show value in $ in the title
        charts.append(self.__create_sum_chart(
            title=TEXT['title_assets_value'],
            adapter=AssetsValues(),
            figure=TreemapFigure(),
            cont_key=self._ASSETS,
            dp_id=TEXT['dp_id_treasury'],
            dp_title=TEXT['dp_title_treasury'],
        ))
        self.__controllers[self._ASSETS][-1].layout.configuration.disable_subtitles()

        # assets without value (other tokens)
        charts.append(self.__create_dataTable(
            title=TEXT['title_assets_novalue'],
            adapter=AssetsTokens(),
            cont_key=self._ASSETS
        ))
 
        return charts

    def __create_chart(self, title: str, adapter: IMetricAdapter, figure: Figure
    , cont_key: int, css_classes: List[str] = [], showOnlyOnAll: bool = False) -> Callable:
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
            adapter=adapter,
        )

        self.__controllers[cont_key].append(controller)
        return layout.get_layout

    def __create_sum_chart(self, 
        title: str,
        adapter: IMetricAdapter,
        figure: Figure,
        cont_key: int,
        dp_id: str,
        dp_title: str,
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
