import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from django_plotly_dash import DjangoDash

app = DjangoDash('SkipDash')

table = dash_table.DataTable(

)

app.layout = html.Div([
    table,
    'text'
])