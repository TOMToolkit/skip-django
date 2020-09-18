from datetime import datetime

import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as dhc
from dash_table import DataTable
from django.conf import settings
from django_plotly_dash import DjangoDash

from skip_dpd.skip_client import get_client

app = DjangoDash('SkipDash', external_stylesheets=[dbc.themes.BOOTSTRAP], add_bootstrap_links=True)


def get_alert_title(alert):
    try:
        if alert['topic'] == 'gcn':
            return alert['message']['What']['Description']
        elif alert['topic'] == 'lvc-counterpart':
            return alert['message']['title']
        elif alert['topic'] == 'tns':
            return f"{alert['identifier']} - {alert['message']['hostname']}"
    except:
        return ''
    return ''

def get_alert_detail_link(alert):
    if alert['topic'] == 'tns':
        return f"[{alert['id']}](http://wis-tns.weizmann.ac.il/object/{alert['message']['name']})"
    else:
        return f"[{alert['id']}](http://skip.dev.hop.scimma.org/api/alerts/{alert['id']})"

skip_client = get_client()()
alerts = skip_client.get_alerts(page=1, page_size=settings.DEFAULT_PAGE_SIZE)
for alert in alerts:
    alert['title'] = get_alert_title(alert)
    alert['id'] = get_alert_detail_link(alert)
topics = [{'label': topic['name'], 'value': topic['id']} for topic in skip_client.get_topics()]

columns = [
    {'id': 'id', 'name': 'Id', 'type': 'text', 'presentation': 'markdown'},
    {'id': 'title', 'name': 'Title'},
    {'id': 'topic', 'name': 'Topic'},
    {'id': 'alert_timestamp', 'name': 'Alert Timestamp'},
    {'id': 'right_ascension', 'name': 'Right Ascension'},
    {'id': 'declination', 'name': 'Declination'},
]


app.layout = dbc.Container([
    dhc.Div(
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='topic-filter',
                    options=topics,
                    placeholder='Select topic to filter.',
                    multi=True
                ),
            ),
            dbc.Col(dcc.DatePickerRange(
                id='time-filter',
                min_date_allowed=datetime(2020, 1, 1),
                initial_visible_month=datetime.now(),
                clearable=True,
                ),
            ),
            dbc.Col(dcc.Input(
                id='cone-search',
                type='text',
                placeholder='Cone Search: RA, Dec, Radius',
                debounce=True
            )),
            dbc.Col(dcc.Input(
                id='keyword-search',
                type='text',
                placeholder='keywords',
                debounce=True
            )),
            dbc.Col(dcc.Input(
                id='event-trig-num-search',
                type='text',
                placeholder='LVC Event Trigger Number',
                debounce=True
            )),
        ],
            style={
                'padding': '10px 0px',
                'justify-content': 'center',
                'align-items': 'center',
                'display': 'flex',
            }
        ),
        style={
            #'text-align': 'center',
        }
    ),
    dhc.Div([
        DataTable(id='alerts-table', columns=columns, data=alerts, page_current=0, page_size=settings.DEFAULT_PAGE_SIZE,
                  page_action='custom',
                  style_data={
                      'whiteSpace': 'normal',
                      'height': 'auto',
                      'maxWidth': '20%'
                  },
                  style_data_conditional=[{
                      'if': {'column_id': 'id'},
                      'vertical-align': 'middle',
                      'padding': '10px 10px 0px 10px',
                      'text-align': 'right',
                  }],
                  style_cell_conditional=[{
                      'if': {'column_id': 'id'},
                      'vertical-align': 'middle',
                      'padding': '10px 10px 0px 10px',
                      'text-align': 'right',
                  }],
                  style_cell={'padding': '0px 10px 0px 0px',
                              'text-align': 'right'},
                #   style_table={'height': '800px'},
                  markdown_options={'link_target': '_parent',},
                  ),
        dcc.Input(id='alerts-table-page-size', type='number', min=10, max=1000, value=settings.DEFAULT_PAGE_SIZE)
        ]
    )
])

# target_page_app.layout = dbc.Container([
#     dhc.Div('hello world')
# ])


# TODO: don't display pagination if total_count < page_size
# TODO: Add keyword search, add backend support - talk to Adam about implementation details
@app.callback(
    Output('alerts-table', 'data'),
    [Input('alerts-table', 'page_current'),
     Input('alerts-table-page-size', 'value'),
     Input('topic-filter', 'value'),
     Input('time-filter', 'start_date'),
     Input('time-filter', 'end_date'),
     Input('cone-search', 'value'),
     Input('keyword-search', 'value'),
     Input('event-trig-num-search', 'value')])
def filter_table(page_current, page_size, topic_filter, start_date, end_date, cone_search, keyword_search, etn_search):
    # Filter parameters keywords must match skip.AlertFilter properties
    filter_parameters = {}
    filter_parameters['page_size'] = page_size if page_size else settings.DEFAULT_PAGE_SIZE
    filter_parameters['topic'] = topic_filter if topic_filter else []
    filter_parameters['alert_timestamp_after'] = start_date if start_date else ''
    filter_parameters['alert_timestamp_before'] = end_date if end_date else ''
    filter_parameters['cone_search'] = cone_search if cone_search else ''
    filter_parameters['keyword'] = keyword_search if keyword_search else ''
    filter_parameters['event_trigger_number'] = etn_search if etn_search else ''
    print(filter_parameters)

    filtered_alerts = skip_client.get_alerts(page=page_current+1, **filter_parameters)
    for filtered_alert in filtered_alerts:
        filtered_alert['title'] = get_alert_title(filtered_alert)
        filtered_alert['id'] = get_alert_detail_link(filtered_alert)
    return filtered_alerts
