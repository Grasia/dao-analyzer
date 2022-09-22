"""
   Descp: This file is used to store color values and functions related to.

   Created on: 30-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""

from typing import Tuple


DARK_BLUE = '#2471a3'
LIGHT_BLUE = '#d4e6f1'
DARK_RED = '#F44336'
LIGHT_RED = '#EF9A9A'
DARK_GREEN = '#4CAF50'
LIGHT_GREEN = '#A5D6A7'
DARK_PURPLE = '#9C27B0'
LIGHT_PURPLE = '#CE93D8'
LIGHT_YELLOW = '#FFF59D'
DARK_YELLOW = '#FFEB3B'
LIGHT_ORANGE = '#FFCC80'
DARK_ORANGE = '#FF9800'
BLACK = 'black'
WHITE = 'white'
GRID_COLOR = '#B0BEC5'
TICKFONT_COLOR = '#696969'


def hex_to_rgba(color: str, alpha: float = 1.0) -> Tuple:
    color = color.lstrip('#')
    color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    color = color + (alpha,)

    return color
