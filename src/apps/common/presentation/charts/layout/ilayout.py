import abc

from dash import html

class ILayout(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_layout(self) -> html.Div: 
        raise NotImplementedError

    @classmethod
    def pane_id(cls) -> int:
        pane_id: int = cls.PANE_ID
        cls.PANE_ID += 1
        return pane_id