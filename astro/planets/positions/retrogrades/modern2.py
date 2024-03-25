# coding=utf-8
"""
Created on 2020, April 16th
@author: orion
"""
import io
from base64 import b64encode
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import numpy as np
import plotly.express as px
import pandas as pd

from astro.constants import BODIES_COLORS


def get_body_color(body):
    return BODIES_COLORS[body]


def get_data():
    data = dict(
        year=[
            "2020",
            "2020",
            "2020",
            "2020",
            # "2020",
            # "2020",
            # "2020",
            # "2020",
            # "2020",
            # "2020",
        ],
        retrograde=[
            "1",
            "2",
            "3",
            "1",
            # "",
            # "",
            # "",
            # "",
            # "",
            # "",
        ],

        contents=[
            "{:10} {:5} {:12}<BR>{:10} {:5} {:12}".format(
                "17/02/2020",
                "12°62",
                "pisces",
                "12/03/2020",
                "29°18",
                "aquarius",

            ),
            "{:10} {:5} {:12}<BR>{:10} {:5} {:12}".format(
                "17/02/2020",
                "12°62",
                "pisces",
                "12/03/2020",
                "29°18",
                "aquarius",

            ),
            "{:10} {:5} {:12}<BR>{:10} {:5} {:12}".format(
                "17/02/2020",
                "12°62",
                "pisces",
                "12/03/2020",
                "29°18",
                "aquarius",

            ),
            "{:10} {:5} {:12}<BR>{:10} {:5} {:12}".format(
                "17/02/2020",
                "12°62",
                "pisces",
                "12/03/2020",
                "29°18",
                "aquarius",

            ),
            # "",
            # "",
            # "",
            # "",
            # "",
            # "",
        ],

        planet=[
            "Mercury",
            "Mercury",
            "Mercury",
            "Venus",
            # "Mars",
            # "Jupiter",
            # "Saturn",
            # 'Uranus',
            # "Neptune",
            # "Pluto",
        ],

    )

    return pd.DataFrame(data)


def get_retrogrades(date):
    df = get_data()

    fig = px.treemap(
        df,
        # path=["year", 'planet', 'retrograde', "date", "zodiac"],
        path=["year", 'planet', 'retrograde', 'contents'],

        # values='end',
        # color='color',
        color_discrete_map={
            '(?)': 'white',
            'Mercury': get_body_color("mercury"),
            'Mars': get_body_color("mars"),
            'Venus': get_body_color("venus"),
            'Jupiter': get_body_color("jupiter"),
            'Saturn': get_body_color("saturn"),
            'Uranus': get_body_color("uranus"),
            'Neptune': get_body_color("neptune"),
            'Pluto': get_body_color("pluto"),

        },
    )

    fig.layout.hovermode = False
    fig.write_json("modern2_retrogrades.json")
    return {'data': fig.data, 'layout': fig.layout}


df = pd.DataFrame([
    dict(Task="Retrograde 1", Start='2009-01-01', End='2009-02-28', Planet="mercury"),
    dict(Task="Retrograde 2", Start='2009-03-05', End='2009-04-15', Planet="mercury"),
    dict(Task="Retrograde 3", Start='2009-07-05', End='2009-08-15', Planet="mercury"),
    dict(Task="Retrograde 1", Start='2009-02-20', End='2009-05-30', Planet="jupiter")
])

fig = px.timeline(df, x_start="Start", x_end="End", y="Planet", color="Planet")

fig.update_xaxes(
    showspikes = True, spikedash = 'solid', spikemode = 'across',
    spikecolor = "grey", spikesnap = "cursor", spikethickness = 2,
)
fig.write_json("modern2-timeline.json")
#
#
# def selection_fn(trace,points,selector):
#     t.data[0].cells.values = [df.loc[points.point_inds][col] for col in ['ID','Classification','Driveline','Hybrid']]
#
# fig.write_html(
#     "{}.html".format(
#         "modern2",
#     ),
# )

# x_data = np.linspace(0, 500, 500)
# y_data = np.random.rand(500)
# height = max(y_data)


app = dash.Dash()

app.layout = html.Div(
    [
        dcc.Graph(id='timeline_graph', figure=fig),
        dcc.Graph(id='retrogrades_graph', figure=fig),
    ],
)


@app.callback(dash.dependencies.Output('retrogrades_graph', 'figure'),
              [dash.dependencies.Input('timeline_graph', 'hoverData')])
def update_graph(hoverData):
    if hoverData:
        date = hoverData['points'][0]['x']
        opacity = 0.8
        res = get_retrogrades(date)
    else:
        res = {'data': [], 'layout': None}
    return res


if __name__ == '__main__':
    app.run_server(debug=True)
