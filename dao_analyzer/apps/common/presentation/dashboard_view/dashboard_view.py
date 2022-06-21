"""
   Descp: It's used to create the dashboard view.

   Created on: 20-feb-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import os
from typing import Dict, List, Callable
from dash import dcc, html
import dash_bootstrap_components as dbc
from dao_analyzer.apps.common.business.transfers.organization import Organization, OrganizationList
from dao_analyzer.apps.common.business.transfers.organization.organization_filter import NetworkFilters, OrganizationFilterGroup
from dao_analyzer.apps.common.business.transfers.organization.participation_stats import ParticipationStat
from dao_analyzer.apps.common.business.transfers.organization.platform import Platform

from dao_analyzer.apps.common.resources import colors as COLOR
from dao_analyzer.apps.common.resources.strings import TEXT
from dao_analyzer.apps.common.presentation.main_view.main_view import REL_PATH

__ECOSYSTEM_SELECTED: Dict[str, List[str]] = {
    'default': ['', '', ''],
    'daohaus': ['daohaus-selected', '', ''],
    'aragon': ['', 'aragon-selected', ''],
    'daostack': ['', '', 'daostack-selected'],
}

def generate_layout(platform: Platform, sections: Dict, datapoints, ecosystem: str, update: str, platform_id: str, org_value: str) -> List:
    """
    Use this function to generate the app view.
    Params:
        labels: A list of dictionaries for each element, in order to 
        fill the dropdown selector.
    Return:
        A html.Div filled with the app view 
    """
    if not org_value:
        org_value = platform.get_default_org_value()

    return html.Div([
        dbc.Container(
            __generate_header(platform, ecosystem, update, org_value),
        className='top body mb-3 py-4'),
        dbc.Container([
            __generate_subheader(platform_id, platform, datapoints),
            __generate_sections(sections),
        ], className='body', id=f'{platform_id}-body'),
    ])

def __gen_ecosystem(id: str, selected: str) -> html.Div:
    return html.Div(children=[
        html.Div(className=f'ecosystem-overlay {id}-color',
            id=f'{id}-bt'),
        html.Img(src=os.path.join(REL_PATH, TEXT[f'{id}_image_name']),
            className='ecosystem-img'),
    ], className=f'ecosystem {id}-ecosystem {selected}')

def __generate_header(platform: Platform, ecosystem: str, update: str, org_value: str) -> dbc.Row:
    selected: List[str] = __ECOSYSTEM_SELECTED['default']
    if ecosystem in __ECOSYSTEM_SELECTED.keys():
        selected = __ECOSYSTEM_SELECTED[ecosystem]

    ecosystems: List[html.Div] = [ __gen_ecosystem(eid, selected[i]) for i,eid in enumerate(['daohaus', 'aragon', 'daostack']) ]

    if not org_value:
        org_value = OrganizationList.ALL_ORGS_ID
    
    # Disable filters if generating header with a DAO pre-selected (comes from URL)
    # If we don't disable the filter, the DAO will be inmediately filtered out
    # Fixes #85
    filterGroup: OrganizationFilterGroup = platform.get_filter_group(
        force_disabled=not OrganizationList.is_all_orgs(org_value)
    )

    networkFilters: NetworkFilters = platform.get_network_filters()

    return dbc.Row(children=[
        html.Div(
            html.Div([
                html.Div(TEXT['ecosystem_selector_title']),
                html.Div(children=ecosystems, className='ecosystems-wrapper'),
            ], className='select-platform-wrapper'),
        className='col d-flex justify-content-center'),
        html.Div(
            html.Div(children=[
                html.Div(html.Span(TEXT['dao_selector_title'])),
                html.Div([
                    dcc.Checklist(
                        options = filterGroup.get_options(),
                        value = filterGroup.get_value(),
                        className='checklist-filter d-flex flex-column',
                        id='org-filter',
                    ),
                    dcc.Checklist(
                        options = networkFilters.get_options(),
                        value = networkFilters.get_value(),
                        className='checklist-filter',
                        id='org-network-filter',
                    ),
                    html.Div(dcc.Dropdown(
                        id='org-dropdown',
                        options=platform.get_dropdown_representation(),
                        value=org_value,
                        clearable=False,
                    )),
                    html.Div("", id='org-number', className='number-of-daos'),
                ], className='flex-grow-1'),
            ], className='select-dao-wrapper'),
        className='col d-flex justify-content-center'),
        dcc.Store(
            id='platform-store',
            data=platform,
            storage_type='memory',
        ),
        html.Div(f'Last update: {update}', className='last-update'),
    ], className='body-header row-divider')

### SUBHEADER THINGS
def _gen_participation_stats(stats: List[ParticipationStat]) -> html.Div:
    children = []
    for s in stats:
        if s.value is None:
            children.append(html.Div(s.text))
        else:
            children.append(html.Div([html.B(s.value_str), s.text]))

    return html.Div(children, className='dao-info-stats')

def _get_platform_info(p: Platform) -> html.Div:
    grid: List[html.Div] = [
        html.Div('Platform', className='dao-info-label'),
        html.Div(p.name, className='dao-info-name'),
        html.Div('Networks', className='dao-info-label'),
        html.Div(', '.join(p.networks), className='dao-info-network'),
    ]

    if p.creation_date:
        grid.append(html.Div("Creation Date", className='dao-info-label'))
        grid.append(html.Div(p.creation_date.strftime(TEXT['creation_date_format']), className='dao-info-date'))

    if p.participation_stats:
        grid.append(html.Div("Participation", className='dao-info-label'))
        grid.append(_gen_participation_stats(p.participation_stats))
    
    return html.Div(grid, className='dao-info-container')

def _get_dao_info(org: Organization) -> html.Div:
    name = html.I(TEXT['unknown_dao_name'])
    if org.get_name():
        name = org.get_name()

    grid: List[html.Div] = [
        html.Div("DAO", className='dao-info-label'),
        html.Div(name, className='dao-info-name'),
        html.Div("Network", className='dao-info-label'),
        html.Div(org.get_network(), className='dao-info-network'),
        html.Div("Address", className='dao-info-label'),
        html.Div(html.Span(org.get_id(), className='address'), className='dao-info-address'),
    ]

    if org.get_creation_date():
        grid.append(html.Div("Creation Date", className='dao-info-label'))
        grid.append(html.Div(org.get_creation_date().strftime(TEXT['creation_date_format']), className='dao-info-date'))
    elif org.get_first_activity():
        grid.append(html.Div("First Activity", className='dao-info-label'))
        grid.append(html.Div(org.get_first_activity().strftime(TEXT['creation_date_format']), className='dao-info-date'))

    if org.get_participation_stats():
        grid.append(html.Div("Participation", className='dao-info-label'))
        grid.append(_gen_participation_stats(org.get_participation_stats()))
    
    return html.Div(grid, className='dao-info-container')

def _gen_sum_hdr(org: Organization = None):
    if not org:
        return None
    
    left = html.Span()
    if org.get_last_activity():
        right = html.Span(['Last active on ', html.B(org.get_last_activity().strftime(TEXT['last_activity_format']))])
    else:
        right = html.Span(['This organization has ', html.B('never'), ' been active'])
    
    return [left, right]

def _get_dao_summary_layout(org_id, datapoints: Dict ):
    dp_divs: List[html.Div] = [ dcc.Loading(
        dp.get_layout(), 
        type='circle',
        color=COLOR.DARK_BLUE
    ) for dp in datapoints.values() ]

    return html.Div([
        html.Div(_gen_sum_hdr(), className='dao-summary-hdr', id=org_id+'-summary-hdr'),
        html.Div(dp_divs, className='dao-summary-body'),
    ], className='dao-summary-container')

def __generate_subheader(org_id: str, platform: Platform, datapoints: Dict[str, List[Callable]]) -> dbc.Row:
    return dbc.Row(
        id=org_id,
        className='my-3',
        children=html.Div([
           dbc.Col(dcc.Loading(html.Div(_get_platform_info(platform), id=org_id+'-info'), color=COLOR.DARK_BLUE)),
           dbc.Col(_get_dao_summary_layout(org_id, datapoints)),
        ], className='dao-header-container pt-4'),
    )

def __generate_sections(sections: Dict[str, List[Callable]]) -> dbc.Row:
    tabs: List[dcc.Tab] = []

    for name, data in sections.items():
        charts = list()
        for chart_pane in data['callables']:
            charts.append(chart_pane())

        sec_hdr = dbc.Row(
            [html.Div(name, className='section-title')],
            id=f'{data["css_id"]}-hdr', 
            className='section-hdr'
        )

        if 'disclaimer' in data and data['disclaimer']:
            sec_hdr.children.append(html.Div(data['disclaimer'], className='section-disclaimer'))

        container = dbc.Container(
            class_name='g-4 mt-4',
            children=[
                sec_hdr,
                dbc.Row(children=charts, className='row-cols-1 row-cols-xl-2 gx-5'),
            ],
        )

        tabs.append(dcc.Tab(label=name, children=container))

    return dcc.Tabs(tabs)
