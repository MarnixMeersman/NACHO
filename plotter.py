from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from asteroidStuff import filenames
df = pd.read_csv("/Users/marnixmeersman/Documents/GitHub/NACHO/full_data.csv", sep=",")

app = Dash(__name__)


app.layout = html.Div([
    html.H4('SNR [dB] for all asteroids observing for 30 [min] on each location'),
    dcc.Graph(id="graph"),
    dcc.Checklist(
        id="checklist",
        options='Name',
        value='Name',
        inline=True
    ),
])


@app.callback(
    Output("graph", "figure"),
    Input("checklist", "value"))
def update_line_chart(continents):
    fig = px.line(df,
        x="date", y="SNR_dB", color='Name')
    return fig


app.run_server(debug=False)