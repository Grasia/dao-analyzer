from dash import html

from dao_analyzer.apps.common.resources.strings import TEXT

class DataPointLayout:
    def __init__(self, css_id, title):
        self._id = css_id
        self._title = title

    @staticmethod
    def _get_dp_icon(evolution: float):
        if evolution is None:
            return

        try:
            if evolution < 0:
                return html.I(className="bi bi-arrow-down-circle-fill dp-icon-down")
            elif evolution > 0:
                return html.I(className="bi bi-arrow-up-circle-fill dp-icon-up")
            else:
                return html.I(className="bi bi-dash-circle dp-icon-same")
        except ValueError:
            return

    def fill_child(
        self,
        number: str = "?",
        evolution: float = None,
        evolution_rel: float = None,
    ):
        evolution_children = []
        if evolution is not None or evolution_rel is not None:
            evolution_children.append(self._get_dp_icon(evolution or evolution_rel))
            evolution_children.append(' ')

        if evolution is not None and evolution_rel is not None:
            evolution_children.append(f'{evolution:.0f} ({abs(evolution_rel):.2f}%)')
        elif evolution is not None:
            evolution_children.append(f'{evolution:.0f}')
        elif evolution_rel is not None:
            evolution_children.append(f'{evolution_rel:.2f}')

        return [
            html.Span(self._title, className="dao-summary-datapoint-title"),
            html.Div(
                number, className="dao-summary-datapoint-number", id=self._id + "-number"
            ),
            html.Div(
                TEXT["this_month"],
                className="dao-summary-datapoint-lastmonth",
            ) if evolution_children else None,
            html.Div(
                evolution_children,
                className="dao-summary-datapoint-evolution",
                id=self._id + "-evolution",
            ) if evolution_children else None,
        ]

    def get_layout(self) -> html.Div:
        return html.Div(self.fill_child(), className='dao-summary-datapoint', id=self._id)

