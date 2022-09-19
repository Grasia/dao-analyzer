from dash.testing.application_runners import import_app

def test_render_component(dash_duo):
    raise NotImplementedError

    app = import_app('dao-analyzer')

    dash_duo.start_server(app)
