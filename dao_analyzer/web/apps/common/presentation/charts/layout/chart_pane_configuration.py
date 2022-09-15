"""
   Descp: Wraps the figure and the chart pane configuration.

   Created on: 14-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List

from dao_analyzer.web.apps.common.presentation.charts.layout.figure.figure_configuration \
    import FigureConfiguration
from .layout_configuration import LayoutConfiguration

class ChartPaneConfiguration(LayoutConfiguration, FigureConfiguration):

    def __init__(self, fig_conf: FigureConfiguration) -> None:
        super().__init__()
        self.__fig_conf = fig_conf
        self.__show_subtitles: bool = True

    @property
    def fig_conf(self) -> FigureConfiguration:
        return self.__fig_conf


    @property
    def show_subtitles(self) -> bool:
        return self.__show_subtitles

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
