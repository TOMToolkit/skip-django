import re

from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as dhc

from django.conf import settings
from django_plotly_dash import DjangoDash

from skip_dpd.skip_client import get_client


app = DjangoDash('SkipSwiftXRTDash', external_stylesheets=[dbc.themes.BOOTSTRAP], add_bootstrap_links=True)

comment_warnings_prefix = 'ranks\.php for details.'
counterpart_identifier_regex = re.compile(r'\d?\w+\s\w\d+\.\d(\+|-)\d+')
comment_warnings_regex = re.compile(r'({prefix}).*$'.format(prefix=comment_warnings_prefix))


def generate_table(alerts):
    table_header = [
        dhc.Thead(
            dhc.Tr([
                dhc.Th(''),
                dhc.Th('Counterpart Identifier'),
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
        alert_id = alert['id']
        ci_match = counterpart_identifier_regex.search(alert['message']['comments'])
        counterpart_identifier = ci_match[0] if ci_match else ''
        cw_match = comment_warnings_regex.search(alert['message']['comments'])
        comment_warnings = cw_match[0][len(comment_warnings_prefix):] if cw_match else ''
        table_rows.append(dhc.Tr([
            dhc.A(alert_id, href=f'/api/alerts/{alert_id}'),
            dhc.Td(counterpart_identifier),
            dhc.Td(alert['right_ascension']),
            dhc.Td(alert['declination']),
            dhc.Td(alert['message'].get('event_trig_num', '')),
            dhc.Td(alert['message'].get('telescope', '')),
            dhc.Td(alert['message'].get('rank', '')),
            dhc.Td(comment_warnings),
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
    alerts = skip_client.get_alerts(page=1, page_size=settings.DEFAULT_PAGE_SIZE,
                                    topic=[lvc_topic['id']], event_trigger_number=event_trigger_number)

    return generate_table(alerts)