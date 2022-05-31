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
from dao_analyzer.apps.common.business.transfers.organization import Organization, OrganizationList, OrganizationFilter

from dao_analyzer.apps.common.resources.strings import TEXT
from dao_analyzer.apps.common.presentation.main_view.main_view import REL_PATH

__ECOSYSTEM_SELECTED: Dict[str, List[str]] = {
    'default': ['', '', ''],
    'daohaus': ['daohaus-selected', '', ''],
    'aragon': ['', 'aragon-selected', ''],
    'daostack': ['', '', 'daostack-selected'],
}

def generate_layout(organizations: OrganizationList, sections: Dict, datapoints, ecosystem: str, update: str, org_id: str, org_value: str) -> List:
    """
    Use this function to generate the app view.
    Params:
        labels: A list of dictionaries for each element, in order to 
        fill the dropdown selector.
    Return:
        A html.Div filled with the app view 
    """
    if not org_value:
        org_value = organizations.get_all_orgs_dict()["value"]

    return html.Div([
        dbc.Container(
            __generate_header(organizations, ecosystem, update, org_value),
        className='top body mb-3 py-4'),
        dbc.Container([
            __generate_subheader(org_id, datapoints),
            __generate_sections(sections),
        ], className='body', id=f'{org_id}-body'),
    ])

def __gen_ecosystem(id: str, selected: str) -> html.Div:
    return html.Div(children=[
        html.Div(className=f'ecosystem-overlay {id}-color',
            id=f'{id}-bt'),
        html.Img(src=os.path.join(REL_PATH, TEXT[f'{id}_image_name']),
            className='ecosystem-img'),
    ], className=f'ecosystem {id}-ecosystem {selected}')

def __generate_header(organizations: OrganizationList, ecosystem: str, update: str, org_value: str) -> dbc.Row:
    selected: List[str] = __ECOSYSTEM_SELECTED['default']
    if ecosystem in __ECOSYSTEM_SELECTED.keys():
        selected = __ECOSYSTEM_SELECTED[ecosystem]

    ecosystems: List[html.Div] = [ __gen_ecosystem(eid, selected[i]) for i,eid in enumerate(['daohaus', 'aragon', 'daostack']) ]

    filters: OrganizationFilter = organizations.get_filters()

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
                        options = {x.id:x.title for x in filters},
                        value = [x.id for x in filters if x.enabled],
                        id='org-filter',
                    ),
                    html.Div(dcc.Dropdown(
                        id='org-dropdown',
                        options=organizations.get_dict_representation(),
                        value=org_value,
                        clearable=False,
                    )),
                    html.Div("", id='org-number', className='number-of-daos'),
                ], className='flex-grow-1'),
            ], className='select-dao-wrapper'),
        className='col d-flex justify-content-center'),
        dcc.Store(
            id='org-store',
            data=organizations,
            storage_type='memory',
        ),
        html.Div(f'Last update: {update}', className='last-update'),
    ], className='body-header row-divider')

### SUBHEADER THINGS
def _get_dao_info(org: Organization) -> html.Div:
    name = html.I(TEXT['unknown_dao_name'])
    if org.get_name():
        name = org.get_name()

    grid: List[html.Div] = [
        html.Div("Name", className='dao-info-label'),
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
        grid.append(html.Div(["Participation", html.Br(), "stats"], className='dao-info-label'))
        children = []
        for s in org.get_participation_stats():
            children.append(html.Div([html.B(s.value_str), s.text]))
        grid.append(html.Div(children, className='dao-info-stats'))
    
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
    dp_divs: List[html.Div] = [ dp.get_layout() for dp in datapoints.values() ]

    return html.Div([
        html.Div(_gen_sum_hdr(), className='dao-summary-hdr', id=org_id+'-summary-hdr'),
        html.Div(dp_divs, className='dao-summary-body'),
    ], className='dao-summary-container', style={'padding': '1em'})

def __generate_subheader(org_id: str, datapoints: Dict[str, List[Callable]]) -> dbc.Row:
    return dbc.Row(
        id=org_id,
        className='my-3',
        children=html.Div([
           html.Div(html.Div(TEXT['no_data_selected'], className='dao-info-name'), id=org_id+'-info'),
           _get_dao_summary_layout(org_id, datapoints)
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
