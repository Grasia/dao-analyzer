"""
   Descp: Common pane which wraps chart layouts.

   Created on: 09-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import dash_html_components as html
import dash_core_components as dcc
from typing import Dict, List

from src.apps.daostack.resources.strings import TEXT
import src.apps.daostack.resources.colors as Color
from src.apps.daostack.presentation.charts.chart_layout import ChartLayout


class ChartPaneLayout():

    def __init__(self, title: str, css_id: str, figure: ChartLayout) -> None:
        self.__title = title
        self.__css_id = css_id
        self.__figure = figure


    def get_layout(self, amount: str, subtitle: str, is_subsection: bool = True) -> html.Div:

        hide: str = '' if show_subsection else 'hide'

        children: List = [html.Span(title, className='graph-title1')]
        children.append(html.Span(
            amount, 
            id=f'{css_id}-amount', 
            className=f'graph-title2 {hide}'))
        children.append(html.Span(
            subtitle, 
            id=f'{css_id}-subtitle',
            className=hide))

        children.append(dcc.Loading(
            type="circle",
            color=Color.DARK_BLUE,
            children=dcc.Graph(id=f'{css_id}-graph', figure=figure_gen())))

        return html.Div(children=children, className='pane graph-pane')
