from datetime import datetime

import dash
from dash.dependencies import Input, Output
from dash_bootstrap_components import Col, Container, Row, themes
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash_html_components import Div
from dash_table import DataTable
from django_plotly_dash import DjangoDash
# import dash_table

from skip_dpd.skip_api_client import SkipAPIClient

app = DjangoDash('SkipDash', external_stylesheets=[themes.BOOTSTRAP], add_bootstrap_links=True)

DEFAULT_PAGE_SIZE = 100

skip_client = SkipAPIClient()
alerts = skip_client.get_alerts()

columns = [
    {'id': 'topic', 'name': 'Topic'},
    {'id': 'alert_timestamp', 'name': 'Alert Timestamp'},
    {'id': 'right_ascension', 'name': 'Right Ascension'},
    {'id': 'declination', 'name': 'Declination'},
]


app.layout = dbc.Container([
    Div(
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='topic-filter',
                options=[
                    {'label': 'gcn', 'value': '1'},
                    {'label': 'tns', 'value': '2'}
                ],
            )),
            dbc.Col(dcc.DatePickerRange(
                id='time-filter',
                min_date_allowed = datetime(2020, 1, 1),
                initial_visible_month = datetime.now()
            )),
            dbc.Col(dcc.Input(
                id='cone-search',
                type='text',
                placeholder='RA, Dec, Radius',
                debounce=True
            )),
        ])
    ),
    Div([
        DataTable(id='alerts-table', columns=columns, data=alerts, page_current=0, page_size=DEFAULT_PAGE_SIZE,
                  page_action='custom', style_table={'height': '800px', 'overflowY': 'auto'}),
        dcc.Input(id='alerts-table-page-size', type='number', min=10, max=1000, value=20)
        ], style={'height': 1000}
    )
])


# TODO: don't display pagination if total_count < page_size
# TODO: Add keyword search, add backend support - talk to Adam about implementation details
@app.callback(
    Output('alerts-table', 'data'),
    [Input('alerts-table', 'page_current'),
     Input('alerts-table-page-size', 'value'),
     Input('alerts-table', 'filter_query'),
     Input('topic-filter', 'value'),
     Input('time-filter', 'start_date'),
     Input('time-filter', 'end_date'),
     Input('cone-search', 'value')])
def filter_table(page_current, page_size, filter_str, topic_filter, start_date, end_date, cone_search):
    print(page_size)
    print(cone_search)
    filter_parameters = {}
    filter_parameters['page_size'] = page_size if page_size else DEFAULT_PAGE_SIZE
    filter_parameters['topic'] = topic_filter if topic_filter else ''
    filter_parameters['alert_timestamp_after'] = start_date if start_date else ''
    filter_parameters['alert_timestamp_before'] = end_date if end_date else ''
    filter_parameters['cone_search'] = cone_search if cone_search else ''

    return skip_client.get_alerts(page=page_current+1, **filter_parameters)