import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_table
# import dash_bootstrap_components as dbc

from django_plotly_dash import DjangoDash

from .skip_api_client import SkipAPIClient

app = DjangoDash('SkipDash')

PAGE_SIZE=100

skip_client = SkipAPIClient()
alerts = skip_client.get_alerts()
# print(alerts['results'])

columns = [
    {'id': 'topic', 'name': 'Topic'},
    {'id': 'alert_timestamp', 'name': 'Alert Timestamp'},
    {'id': 'right_ascension', 'name': 'Right Ascension'},
    {'id': 'declination', 'name': 'Declination'}
]

app.layout = dash_table.DataTable(
        id='alerts_table',
        columns=columns,
        data=alerts,
        page_current=0,
        page_size=PAGE_SIZE,
        page_action='custom'
    )

@app.callback(
    Output('alerts_table', 'data'),
    [Input('alerts_table', 'page_current'),
     Input('alerts_table', 'page_size')])
def update_table(page_current, page_size):
    return skip_client.get_alerts(page=page_current+1, limit=page_size)
    