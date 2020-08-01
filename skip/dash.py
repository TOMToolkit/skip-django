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

columns = [
    {'id': 'topic', 'name': 'Topic'},
    {'id': 'alert_timestamp', 'name': 'Alert Timestamp'},
    {'id': 'right_ascension', 'name': 'Right Ascension'},
    {'id': 'declination', 'name': 'Declination'}
]

topic_mapping = {
    'gcn': 1,
    'tns': 2
}

# operators = ['>=', '<=', '<', '>', '!=', '=', 'contains', 'datestartswith']
valid_operators = ['=', 'contains']

def split_filter_query(filter_query):
    for operator_type in valid_operators:
        for operator in operator_type:
            if operator in filter_query:
                name, value = filter_query.split(operator, 1)
                name = name[name.find('{') + 1: name.rfind('}')]
                value = value.strip()
                v0 = value[0]
                if (v0 == value[-1] and v0 in ("'", '"', '`')):
                    value = value[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        value = value

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

app.layout = dash_table.DataTable(
        id='alerts_table',
        columns=columns,
        data=alerts,
        page_current=0,
        page_size=PAGE_SIZE,
        page_action='custom',
        filter_action='custom',
        filter_query='',
        style_table={'height': '300px', 'overflowY': 'auto'}
    )

# TODO: Update backend with limit param, add page_size parameter to dash_table
@app.callback(
    Output('alerts_table', 'data'),
    [Input('alerts_table', 'page_current'),
     Input('alerts_table', 'page_size'),
     Input('alerts_table', 'filter_query')])
def filter_table(page_current, page_size, filter):
    filter_parameters = {}
    for filter_query in filter.split(' && '):
        
        column, operator, filter_value = split_filter_query(filter_query)
        if operator in valid_operators:
            if column == 'topic':
                filter_parameters[column] = topic_mapping[filter_value]
            else:
                filter_parameters[column] = filter_value
        
    return skip_client.get_alerts(page=page_current+1, limit=page_size, **filter_parameters)