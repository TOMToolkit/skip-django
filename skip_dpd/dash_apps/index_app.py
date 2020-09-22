from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as dhc
from django_plotly_dash import DjangoDash
from django.urls import reverse_lazy


app = DjangoDash('SkipDash', external_stylesheets=[dbc.themes.BOOTSTRAP], add_bootstrap_links=True)


app.layout = dbc.Container([
    dhc.Div(
        dbc.Row([
            dbc.Col(
                dhc.A('View All Alerts', href='/alerts', target='_top')
            ),
            dbc.Col(
                dhc.A('View Swift XRT Alerts', href='/swift', target='_top')
            )
        ])
    )
])
