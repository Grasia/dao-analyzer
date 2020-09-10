"""
   Descp: Wraps the layout and its control.

   Created on: 09-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from src.apps.daostack.presentation.charts.chart import Chart
from src.apps.daostack.presentation.charts.chart_pane_layout \
    import ChartPaneLayout
from src.apps.daostack.presentation.charts.chart_controller import ChartController


class BarChart(Chart):

    def __init__(self) -> None:
        super().__init__()
        css_id: str = f'pane{Chart.ID}'
        self.__layout = ChartPaneLayout()


    def get_layout(self) -> Any:
        """
        Returns an empty layout. 
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_layout_configuration(self) -> ChartConfiguration:
        """
        Returns the layout configuration.
        """
        raise NotImplementedError


    @abc.abstractmethod
    def enable_subtitles(self) -> ChartConfiguration:
        """
        Enables the pane subtitles.
        """
        raise NotImplementedError


    @abc.abstractmethod
    def disable_subtitles(self) -> ChartConfiguration:
        """
        Disables the pane subtitles. 
        """
        raise NotImplementedError