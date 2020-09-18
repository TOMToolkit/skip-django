from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as dhc

from django.conf import settings
from django_plotly_dash import DjangoDash

from skip_dpd.skip_client import get_client


app = DjangoDash('SkipSwiftXRTDash', external_stylesheets=[dbc.themes.BOOTSTRAP], add_bootstrap_links=True)

def generate_table(alerts):
    table_header = [
        dhc.Thead(
            dhc.Tr([
                # dhc.A(href=)
                dhc.Th('Right Ascension'),
                dhc.Th('Declination'),
                dhc.Th('LIGO Event TrigNum'),
                dhc.Th('Telescope'),
                dhc.Th('Rank'),
                dhc.Th('Comments'),
            ])
        )
    ]
    table_rows = []
    for alert in alerts:
        table_rows.append(dhc.Tr([
            dhc.Td(alert['right_ascension']),
            dhc.Td(alert['declination']),
            dhc.Td(alert['message'].get('event_trig_num', '')),
            dhc.Td(alert['message'].get('telescope', '')),
            dhc.Td(alert['message'].get('rank', '')),
            dhc.Td(alert['message']['comments']),
        ]))
    return dbc.Table(table_header + table_rows, bordered=True)


skip_client = get_client()()
lvc_topic = skip_client.get_topics(name='lvc-counterpart')[0]
print(lvc_topic)
alerts = skip_client.get_alerts(page=1, page_size=settings.DEFAULT_PAGE_SIZE, topic=[lvc_topic['id']])


app.layout = dhc.Div([
    dcc.Input(
        id='event-trigger-number',
        type='text',
        placeholder='test'
    ),
    dhc.Div(generate_table(alerts), id='table-container'),
])


@app.callback(
    Output('table-container', 'children'),
    [Input('event-trigger-number', 'value')]
)
def update_table(event_trig_num):
    event_trigger_number = event_trig_num if event_trig_num else ''
    alerts = skip_client.get_alerts(page=1, page_size=200,
                                    topic=[lvc_topic['id']], event_trigger_number=event_trigger_number)

    return generate_table(alerts)