from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as dhc
from django_plotly_dash import DjangoDash


target_page_app = DjangoDash('SkipTargetDash')

target_page_app.layout = dhc.Div([
    dcc.Location(id='url', refresh=True),
    dhc.Div(
        dbc.Row([
            dhc.A('Back', href='/skip/', id='back-link', target='_parent')
        ])
    ),
    dhc.Div(
        dbc.Row([
            dbc.Col([
                dbc.Row(
                    dhc.Dl([
                        dhc.Dt('Name'),
                        dhc.Dd('', id='name-data-definition')
                    ], id='target-datalist')
                )
            ])
        ])
    )
])

@target_page_app.expanded_callback(
    Output('name-data-definition', 'value'),
    [Input('url', 'pathname')]
)
def target_page_app_data(pathname, **kwargs):
    print(f'location: {pathname}')
    print(kwargs.items())
    print(kwargs['request'].POST.dict())