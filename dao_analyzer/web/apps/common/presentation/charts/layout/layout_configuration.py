import dao_analyzer.web.apps.common.resources.colors as Color

class LayoutConfiguration:
    def __init__(self) -> None:
        self.__color: str = Color.DARK_BLUE
        self.__css_border: str = ''
    
    @property
    def css_border(self) -> str:
        return self.__css_border

    @property
    def color(self) -> str:
        return self.__color

    def set_color(self, color: str) -> None:
        if color:
            self.__color = color

    def set_css_border(self, css_border: str) -> None:
        self.__css_border = css_border