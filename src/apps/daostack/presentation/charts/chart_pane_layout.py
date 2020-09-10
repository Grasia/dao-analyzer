"""
   Descp: Common pane which wraps chart layout and other components.

   Created on: 09-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

import dash_html_components as html
import dash_core_components as dcc
from typing import List, Dict

from src.apps.daostack.resources.strings import TEXT
import src.apps.daostack.resources.colors as Color
from src.apps.daostack.presentation.charts.chart_layout import ChartLayout
from src.apps.daostack.presentation.charts.chart_configuration\
.chart_configuration import ChartConfiguration


class ChartPaneLayout():
    SUFFIX_ID_CHART: str = '-chart'
    SUFFIX_ID_SUBTITLE1: str = '-subtitle1'
    SUFFIX_ID_SUBTITLE2: str = '-subtitle2'

    def __init__(self, title: str, css_id: str, figure: ChartLayout) -> None:
        self.__title: str = title
        self.__css_id: str = css_id
        self.__figure: ChartLayout = figure
        self.__show_subtitles: bool = True


    def get_layout(self, plot_data) -> html.Div:
        """
        Returns a pane with all the components initialized .
        """
        figure: Dict = self.__figure.get_empty_layout()
        subtitle1: str = TEXT['default_amount']
        subtitle2: str = TEXT['no_data_selected']
        children = self._get_children(subtitle1, subtitle2, figure)

        return html.Div(
            children=children, 
            id=self.__css_id, 
            className='pane graph-pane'
        )


    def fill_child(self, plot_data: Dict) -> List:
        figure = self.__figure.get_layout(plot_data = plot_data)
        subtitle1: str = TEXT['default_amount']
        subtitle2: str = TEXT['no_data_selected']

        if self.__show_subtitles:
            subtitle1 = TEXT['graph_amount'].format(
                plot_data['last_serie_elem'], 
                plot_data['last_value']
            )
            subtitle2 = TEXT['graph_subtitle'].format(plot_data['diff'])

        return self._get_children(subtitle1, subtitle2, figure)


    def _get_children(self, subtitle1, subtitle2, figure) -> List:
        hide: str = '' if self.__show_subtitles else 'hide'

        return [
            html.Span(
                self.__title,
                className = 'graph-pane-title'
            ),
            html.Span(
                subtitle1,
                id = f'{self.__css_id}{self.SUFFIX_ID_SUBTITLE1}',
                className = f'graph-pane-subtitle {hide}'
            ),
            html.Span(
                subtitle2, 
                id = f'{self.__css_id}{self.SUFFIX_ID_SUBTITLE2}',
                className = hide
            ),
            dcc.Loading(
                type = "circle",
                color = Color.DARK_BLUE,
                children = dcc.Graph(
                    id = f'{self.__css_id}{self.SUFFIX_ID_CHART}', 
                    figure = figure
                ),
            ),
        ]


    def enable_subtitles(self) -> None:
        self.__show_subtitles = True


    def disable_subtitles(self) -> None:
        self.__show_subtitles = False


    def get_configuration(self) -> ChartConfiguration:
        return self.__figure.get_configuration()
