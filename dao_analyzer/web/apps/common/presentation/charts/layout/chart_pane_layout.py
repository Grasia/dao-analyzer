"""
   Descp: Common pane which wraps chart layout and other components.

   Created on: 09-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from dash import html
from dash import dcc
from typing import List, Dict, Union

from dao_analyzer.web.apps.common.presentation.charts.layout.ilayout import ILayout
from dao_analyzer.web.apps.common.resources.strings import TEXT
from dao_analyzer.web.apps.common.presentation.charts.layout.figure.figure import Figure
from dao_analyzer.web.apps.common.presentation.charts.layout.chart_pane_configuration \
    import ChartPaneConfiguration


class ChartPaneLayout(ILayout):
    PANE_ID: int = 1
    SUFFIX_ID_CHART: str = '-chart'
    SUFFIX_ID_SUBTITLE1: str = '-subtitle1'
    SUFFIX_ID_SUBTITLE2: str = '-subtitle2'


    def __init__(self, title: str, css_id: str, figure: Figure, css_classes: Union[List[str], str] = []) -> None:
        self.__title: str = title
        self.__css_id: str = css_id
        self.__figure: Figure = figure
        if isinstance(css_classes, str):
            self.__css_classes: List[str] = css_classes.split(' ')
        else:
            self.__css_classes: List[str] = css_classes
        self.__configuration: ChartPaneConfiguration = ChartPaneConfiguration(
            figure.configuration)

    def get_layout(self) -> html.Div:
        """
        Returns a pane with all the components initialized .
        """
        figure: Dict = self.__figure.get_empty_figure()
        subtitle1: str = TEXT['default_amount']
        subtitle2: str = TEXT['no_data_selected']
        children = self._get_children(subtitle1, subtitle2, figure)

        return html.Div(
            children=dcc.Loading(
                type="circle",
                color=self.configuration.color,
                children=html.Div(
                    children=children,
                    id=self.__css_id,
                    className='d-flex flex-column'
            )),  
            className=f'pane {self.configuration.css_border} col {" ".join(self.__css_classes)}'
        )


    def fill_child(self, plot_data: Dict = None) -> List:
        if plot_data:
            figure = self.__figure.get_figure(plot_data=plot_data)
        else:
            figure = self.__figure.get_empty_figure()
        subtitle1: str = TEXT['default_amount']
        subtitle2: str = TEXT['no_data_selected']

        if plot_data and self.configuration.show_subtitles:
            subtitle1 = TEXT['graph_amount'].format(
                plot_data['last_serie_elem'], 
                plot_data['last_value']
            )
            subtitle2 = TEXT['graph_subtitle'].format(plot_data['diff_rel'])

        return self._get_children(subtitle1, subtitle2, figure)


    def _get_children(self, subtitle1, subtitle2, figure) -> List:
        hide: str = '' if self.configuration.show_subtitles else 'hide'

        return [
            html.Div(children=[
                html.Span(
                    self.__title,
                    className='graph-pane-title'
                ),
                html.Span(
                    subtitle2, 
                    id=f'{self.__css_id}{self.SUFFIX_ID_SUBTITLE2}',
                    className=f'{hide}'
                ),
            ], className='d-flex flex-column chart-header'),
            dcc.Graph(
                id=f'{self.__css_id}{self.SUFFIX_ID_CHART}',
                figure=figure,
                className='chart',
            ),
        ]


    @property
    def configuration(self) -> ChartPaneConfiguration:
        return self.__configuration


    @property
    def figure(self) -> Figure:
        return self.__figure
