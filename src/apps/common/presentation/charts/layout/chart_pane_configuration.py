"""
   Descp: Wraps the figure and the chart pane configuration.

   Created on: 14-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List

import src.apps.common.resources.colors as Color
from src.apps.common.presentation.charts.layout.figure.figure_configuration \
    import FigureConfiguration

class ChartPaneConfiguration(FigureConfiguration):

    def __init__(self, fig_conf: FigureConfiguration) -> None:
        self.__fig_conf = fig_conf
        self.__show_subtitles: bool = True
        self.__css_border: str = ''
        self.__color: str = Color.DARK_BLUE


    @property
    def fig_conf(self) -> FigureConfiguration:
        return self.__fig_conf


    @property
    def show_subtitles(self) -> bool:
        return self.__show_subtitles


    @property
    def css_border(self) -> str:
        return self.__css_border


    @property
    def color(self) -> str:
        return self.__color


    def enable_legend(self) -> None:
        self.fig_conf.enable_legend()


    def disable_legend(self) -> None:
        self.fig_conf.disable_legend()

    
    def get_legend(self) -> Dict:
        return self.fig_conf.get_legend()


    def add_horizontal_line(self, y: float, y_ref: str) -> None:
        self.fig_conf.add_horizontal_line(y, y_ref)


    def get_shapes(self) -> List[Dict]:
        return self.fig_conf.get_shapes()


    def get_axis_layout(self, args: Dict) -> Dict:
        return self.fig_conf.get_axis_layout(args)


    def enable_subtitles(self) -> None:
        self.__show_subtitles = True


    def disable_subtitles(self) -> None:
        self.__show_subtitles = False


    def set_color(self, color: str) -> None:
        if color:
            self.__color = color


    def set_css_border(self, css_border: str) -> None:
        self.__css_border = css_border
