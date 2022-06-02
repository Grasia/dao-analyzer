"""
   Descp: Wraps the figure configuration.

   Created on: 10-sep-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Dict, List, Tuple

import dao_analyzer.apps.common.resources.colors as Color

class FigureConfiguration():

    def __init__(self) -> None:
        self.__show_legend: bool = True
        self.__horizontal_lines: List[Tuple[float, str]] = list()
        self.__x_layout_params: List[Dict] = [{}]
        self.__y_layout_params: List[Dict] = [{}]


    def enable_legend(self) -> None:
        self.__show_legend = True


    def disable_legend(self) -> None:
        self.__show_legend = False

    
    def get_legend(self) -> Dict:
        legend: Dict = {'orientation': 'h', 'x': 0, 'y': 1.2}
        return legend if self.__show_legend else {}


    def add_horizontal_line(self, y: float, y_ref: str) -> None:
        """
        Adds a horizontal line in the list.
        Params:
            * y: its value in the y-axis
            * y_ref: it selects which y-axis you want, in the case there
                     is more than one. E.g. y, y2, y3, ...
        """
        self.__horizontal_lines.append((y, y_ref))


    def get_shapes(self) -> List[Dict]:
        shapes: List[Dict] = list()

        for y, y_ref in self.__horizontal_lines:
            shapes.append({
                'type': 'line',
                'xref': 'paper',
                'yref': y_ref,
                'x0': 0,
                'y0': y,
                'x1': 1,
                'y1': y,
                'line':{
                    'color': Color.BLACK,
                    'width': 0.5,
                    'dash':'dot'
                }
            })

        return shapes


    def get_x_axis_layout(self, axis: int = 0) -> Dict:
        return self.__get_axis_layout(args=self.__x_layout_params[axis])


    def get_y_axis_layout(self, axis: int = 0) -> Dict:
        return self.__get_axis_layout(args=self.__y_layout_params[axis]) 


    def __get_axis_layout(self, args: Dict) -> Dict:
        """
        Returns the axis layout using params in args.
        TODO: remove args parameter to simplify.
        """
        axis_l: Dict[str, str] = {
            'type': args['type'] if 'type' in args else '-',
            'ticks': 'outside',
            'ticklen': 5,
            'tickwidth': 2,
            'ticksuffix': args['suffix'] if 'suffix' in args else '',
            'showline': True, 
            'linewidth': 2, 
            'linecolor': Color.BLACK,
            'showgrid': args['grid'] if 'grid' in args else False,
            'gridwidth': 0.5,
            'gridcolor': Color.GRID_COLOR,
            'tickfont_color': Color.TICKFONT_COLOR,
            'automargin': True,
        }

        if 'removemarkers' in args:
            axis_l['ticklen'] = 0
            axis_l['tickwidth'] = 0
        if 'tickvals' in args:
            axis_l['tickvals'] = args['tickvals']
        if 'reverse_range' in args:
            axis_l['autorange'] = 'reversed'
        if 'l_range' in args:
            axis_l['range'] = args['l_range']
        if 'tickformat' in args:
            axis_l['tickformat'] = args['tickformat']
        if 'tickangle' in args:
            axis_l['tickangle'] = 45
        if 'matches' in args:
            axis_l['matches'] = args['matches']
        if 'tickfont_size' in args:
            axis_l['tickfont_size'] = args['tickfont_size']

        return axis_l

    def get_height(self) -> int:
        return 350

    def get_margin(self) -> Dict[str, int]:
        # Margin is calculated automatically
        return {
            'l': 0,
            'r': 0,
            't': 0,
            'b': 0,
        }

    def add_axis(self, x_axis: int, y_axis: int) -> None:
        self.__x_layout_params = [{} for _ in range(x_axis)]
        self.__y_layout_params = [{} for _ in range(y_axis)]


    def add_x_params(self, params: Dict, axis: int = 0) -> None:
        self.__add_params(params=params, axis=self.__x_layout_params[axis])


    def add_y_params(self, params: Dict, axis: int = 0) -> None:
        self.__add_params(params=params, axis=self.__y_layout_params[axis])


    def __add_params(self, params: Dict, axis: Dict) -> None:
        for k, v in params.items():
            axis[k] = v
