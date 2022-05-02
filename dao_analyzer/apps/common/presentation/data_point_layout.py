from dash import html

from dao_analyzer.apps.common.resources.strings import TEXT

class DataPointLayout:
    def __init__(self, css_id, title, hide_evolution=False):
        self._id = css_id
        self._title = title
        self._hide_evolution = hide_evolution

    @staticmethod
    def _get_dp_icon(evolution: str):
        if not evolution:
            return

        if evolution.startswith("-"):
            return html.I(className="fa-solid fa-circle-down fa-xs dp-icon-down")
        elif evolution == "0" or evolution == "?":
            return html.I(className="fa-solid fa-circle-minus fa-xs dp-icon-same")
        else:
            return html.I(className="fa-solid fa-circle-up fa-xs dp-icon-up")

    def fill_child(
        self,
        number: str = "?",
        evolution: str = "?",
    ):
        hes = {"display": "none"} if self._hide_evolution else {}
        return [
            html.Span(self._title, className="dao-summary-datapoint-title"),
            html.Div(
                number, className="dao-summary-datapoint-number", id=self._id + "-number"
            ),
            html.Div(
                TEXT["this_month"],
                className="dao-summary-datapoint-lastmonth",
                style=hes,
            ),
            html.Div(
                [self._get_dp_icon(evolution), " ", evolution],
                className="dao-summary-datapoint-evolution",
                id=self._id + "-evolution",
                style=hes,
            ),
        ]

    def get_layout(self) -> html.Div:
        return html.Div(self.fill_child(), className='dao-summary-datapoint', id=self._id)

