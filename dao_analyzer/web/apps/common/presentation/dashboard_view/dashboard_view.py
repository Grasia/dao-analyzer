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

import dao_analyzer_components as dac

from dao_analyzer.web.apps.common.business.transfers.organization import Organization, OrganizationList
from dao_analyzer.web.apps.common.business.transfers.organization.organization_filter import NetworkRadioButton, OrganizationFilterGroup
from dao_analyzer.web.apps.common.business.transfers.organization.participation_stats import ParticipationStat
from dao_analyzer.web.apps.common.business.transfers.organization.platform import Platform

from dao_analyzer.web.apps.common.resources import colors as COLOR
from dao_analyzer.web.apps.common.resources.strings import TEXT
from dao_analyzer.web.apps.common.presentation.main_view.main_view import REL_PATH

__ECOSYSTEM_SELECTED: Dict[str, List[str]] = {
    'default': ['', '', ''],
    'daohaus': ['daohaus-selected', '', ''],
    'aragon': ['', 'aragon-selected', ''],
    'daostack': ['', '', 'daostack-selected'],
}

def generate_layout(
    organization_list: OrganizationList, 
    platform_info: Platform,
    sections: Dict,
    datapoints: List[dac.DataPoint], 
    update: str, 
    platform_id: str, 
    org_value: str,
    network_value: str,
    filter_values: List[str],
) -> List:
    """
    Use this function to generate the app view.
    Params:
        labels: A list of dictionaries for each element, in order to 
        fill the dropdown selector.
    Return:
        A html.Div filled with the app view 
    """
    if not org_value:
        org_value = organization_list.ALL_ORGS_ID

    assert isinstance(platform_info, Platform)

    return html.Div([
        dbc.Container(
            __generate_header(organization_list, platform_info, update, org_value, network_value, filter_values),
        className='top body mb-3 py-4'),
        dbc.Container([
            __generate_subheader(platform_id, datapoints),
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

def __generate_header(
    organization_list: OrganizationList,
    platform_info: Platform,
    update: str,
    org_value: str,
    network_value: str,
    filter_values: List[str],
) -> dbc.Row:
    selected: List[str] = __ECOSYSTEM_SELECTED['default']
    if platform_info.id in __ECOSYSTEM_SELECTED.keys():
        selected = __ECOSYSTEM_SELECTED[platform_info.id]

    ecosystems: List[html.Div] = [ __gen_ecosystem(eid, selected[i]) for i,eid in enumerate(['daohaus', 'aragon', 'daostack']) ]

    if not org_value:
        org_value = OrganizationList.ALL_ORGS_ID
    
    # Disable filters if generating header with a DAO pre-selected (comes from URL)
    # If we don't disable the filter, the DAO will be inmediately filtered out
    # Fixes #85
    filterGroup: OrganizationFilterGroup = organization_list.get_filter_group(
        values=filter_values,
        force_disabled=not OrganizationList.is_all_orgs(org_value),
        diff=True,
    )

    try:
        networkRadio: NetworkRadioButton = organization_list.get_network_radio(network_value)
    except ValueError:
        networkRadio: NetworkRadioButton = organization_list.get_network_radio()

    return dbc.Row(children=[
        # 1. Ecosystem selector
        html.Div(
            html.Div([
                html.Div(TEXT['ecosystem_selector_title']),
                html.Div(children=ecosystems, className='ecosystems-wrapper'),
            ], className='header-selector-wrapper'),
        className='col d-flex justify-content-center'),
        # 2. Network selector
        html.Div(
            html.Div(children=[
                html.Div(html.Span(TEXT['network_selector_title'])),
                dcc.RadioItems(
                    options = networkRadio.get_options(),
                    value = networkRadio.get_value(),
                    className = 'checklist-filter',
                    id='org-network-radio'),
            ], className='header-selector-wrapper'),
        className='col-3 d-flex justify-content-center'),
        # 3. DAO selector (and filtering)
        html.Div(
            html.Div(children=[
                html.Div(TEXT['dao_selector_title']),
                html.Div([
                    dcc.Checklist(
                        options = filterGroup.get_options(),
                        value = filterGroup.get_values(),
                        className='checklist-filter d-flex flex-column',
                        id='org-filter',
                    ),
                    dcc.Dropdown(
                        id='org-dropdown',
                        options=organization_list.get_dict_representation(),
                        value=org_value,
                        clearable=False,
                    ),
                    html.Div("", id='org-number', className='number-of-daos'),
                ], className='dao-dropdown-wrapper'),
            ], className='header-selector-wrapper select-dao-wrapper'),
        className='col d-flex justify-content-center'),
        # 4. information storing (hidden from user)
        # The following dcc is changed in callbacks that modify the dao-info-container
        dcc.Store(
            id='platform-info-store',
            data=platform_info,
            storage_type='memory',
        ),
        # This dcc is read-only an used to generate the dropdown
        dcc.Store(
            id='organization-list-store',
            data=organization_list,
            storage_type='memory',
        ),
        html.Div(f'Last update: {update}', className='last-update'),
    ], className='body-header row-divider')

### SUBHEADER THINGS
def _gen_participation_stats(stats: List[ParticipationStat]) -> List[html.Div]:
    return [ { 'text': s.text, 'value': s.value_str } for s in stats ]

def _aux_crdatetime(date) -> str:
    if date:
        return date.strftime(TEXT['creation_date_format'])
    else:
        return None

def _get_platform_info(p: Platform) -> dac.PlatformInfo:
    if p is None:
        return html.Div(TEXT['no_data_selected'], className='dao-info-name')

    return dac.PlatformInfo(
        name=p.name,
        networks=p.networks,
        creation_date=_aux_crdatetime(p.creation_date),
        participation_stats=_gen_participation_stats(p.participation_stats)
    )

def _get_dao_info(org: Organization) -> dac.DAOInfo:
    return dac.DAOInfo(
        name=org.get_name(), 
        network=org.get_network(),
        address=org.get_id(),
        creation_date=_aux_crdatetime(org.get_creation_date()),
        first_activity=_aux_crdatetime(org.get_first_activity()),
        participation_stats=_gen_participation_stats(org.get_participation_stats()),
    )

def _gen_sum_hdr(org: Organization = None):
    if not org:
        return None
    
    left = html.Span()
    if org.get_last_activity():
        right = html.Span(['Last active on ', html.B(org.get_last_activity().strftime(TEXT['last_activity_format']))])
    else:
        right = html.Span(['This organization has ', html.B('never'), ' been active'])
    
    return [left, right]

def _get_dao_summary_layout(org_id, datapoints: List[dac.DataPoint]):
    dp_divs: List[html.Div] = [ dcc.Loading(
        dp, 
        type='circle',
        color=COLOR.DARK_BLUE
    ) for dp in datapoints ]

    return html.Div([
        html.Div(_gen_sum_hdr(), className='dao-summary-hdr', id=org_id+'-summary-hdr'),
        html.Div(dp_divs, className='dao-summary-body'),
    ], className='dao-summary-container')

def __generate_subheader(org_id: str, datapoints: List[dac.DataPoint]) -> dbc.Row:
    return dbc.Row(
        id=org_id,
        className='my-3',
        children=html.Div([
           dbc.Col(dcc.Loading(html.Div(_get_platform_info(None), id=org_id+'-info'), color=COLOR.DARK_BLUE)),
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
