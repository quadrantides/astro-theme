# coding=utf-8
"""
Created on 2020, December 6th
@author: orion
"""
import os
import datetime
import pandas as pd
import numpy as np
import plotly

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'astro.settings')
django.setup()

from transcend.models.zodiac.constants import get_default as get_default_zodiac
from transcend.views.charts.ephemeris.retrogrades.graphics import Graphic


def get_config():
    return {'displayModeBar': False}
    # return {
    #     "zoom2d": False,
    #     "pan2d": False,
    #     "select2d": False,
    #     "lasso2d": False,
    #     "zoomIn2d": False,
    #     "zoomOut2d": False,
    #     "autoScale2d": False,
    #     "resetScale2d": False,
    #     "hoverClosestPie": False,
    #     "toggleHover": False,
    #     "resetViews": False,
    #     "toggleSpikelines": False,
    #     "hoverClosestCartesian": False,
    #     "hoverCompareCartesian": False,
    # }


def Visualize(start_date, end_date, freq, body):

    # VISUALIZATION

    # retrograde_data = dict(
    #     zodiac=[],
    #     longitude=[],
    #     longitudes_in_zodiac=[],
    #     date=[],
    #     hover_retrograde_period=[],
    # )

    DATE_FORMAT = "%Y"

    width = 750
    height = width

    title = "Rétrogradations de la planète {} entre {} et {}".format(
        body,
        start_date.year,
        end_date.year,
    )

    data = dict(
        zodiac=get_default_zodiac(),
        retrogrades=dict(
            date=dict(
                start=start_date,
                end=end_date,
                freq=freq,
            ),
            body=body,
        ),
    )
    obj = Graphic(data, title)
    obj.create()
    obj.graphic.write_html(
        "retrogrades_{}.html".format(
            body,
        ),
        config=get_config(),
    )
    obj.graphic.write_json(
        "retrogrades_{}.json".format(
            body,
        ),
    )
    config = get_config()
    # d=plotly.offline.plot(
    #     obj.graphic,
    #     filename="retrogrades_{}.html".format(
    #         body,
    #     ),
    #     include_plotlyjs=False,
    #     output_type='div',
    #     image_width=600,
    #     image_height=600,
    #     config=get_config(),
    # )

    print("ok")

    # nb_retrogrades = len(data["begin"]['longitude'])
    #
    # nb_r = 1
    # r0 = 0.25
    # dangle = 20
    #
    # for i, begin in enumerate(data["begin"]["longitude"][1::]):
    #     end = data["end"]['longitude'][i-1]
    #     if begin - end < dangle:
    #         nb_r += 1
    #
    # dr = (1.0 - r0) / nb_r
    #
    # data['r'] = r0 + dr * np.array(list(range(nb_r))) / (nb_r - 1)
    #
    # text = ['{}'.format(date.strftime(DATE_FORMAT)) for date in data["begin"]["date"]]
    # for date in data["end"]["date"]:
    #     text.append(
    #         '{}'.format(date.strftime(DATE_FORMAT)),
    #     )
    #
    # coordinates = [None] * nb_retrogrades
    # for i in range(nb_retrogrades):
    #     coordinates[i] = get_coordinates(data["begin"]['longitude'][i], data['r'][i])
    #
    # r = []
    # theta = []
    # for i in range(nb_retrogrades):
    #     r.append(data['r'][i])
    #     r.append(data['r'][i])
    #     theta.append(data["begin"]['longitude'][i])
    #     theta.append(data["end"]['longitude'][i])
    #
    # traces = []
    #
    # for i in range(nb_retrogrades):
    #
    #     trace = go.Scatterpolar(
    #         visible=True,
    #         r=[data['r'][i], data['r'][i]],
    #         theta=[data["begin"]['longitude'][i], data["end"]['longitude'][i]],
    #         mode='lines',
    #         name=body,
    #         text=[
    #             data["begin"]["date"][i].strftime(DATE_FORMAT),
    #             data["end"]["date"][i].strftime(DATE_FORMAT),
    #         ],
    #     )
    #     traces.append(trace)
    #
    # # annotations = [dict(
    # #     x=0.5 + coordinatesi["x"],
    # #     y=0.5 + coordinatesi["y"],
    # #     text=texti,
    # #     xanchor='center',
    # #     yanchor='middle',
    # #     showarrow=False,
    # # ) for coordinatesi, texti in zip(coordinates, text)]
    #
    # layout = go.Layout(
    #     title=title,
    #     width=width,
    #     height=height,
    #     font=dict(
    #         family='sans-serif',
    #         size=10,
    #         color='#000',
    #     ),
    #     # annotations=annotations,
    #     xaxis=dict(
    #         fixedrange=True,
    #         visible=False,
    #     ),
    #
    #     polar=dict(
    #         domain=dict(
    #             x=[0, 1],
    #             y=[0, 1],
    #         ),
    #         bgcolor="rgb(255, 2555, 255)",
    #         angularaxis=dict(
    #             visible=True,
    #             linewidth=1,
    #             showline=True,
    #             linecolor='#444',
    #             dtick=30,
    #             thetaunit="degrees",
    #             gridcolor="#444",
    #             gridwidth=1,
    #             # showticklabels=False,
    #             ticks='outside',
    #         ),
    #         radialaxis=dict(
    #             visible=False,
    #             tickmode="array",
    #             # tickvals=2 * categoryarray,
    #             showticklabels=False,
    #             side="counterclockwise",
    #             angle=0,
    #             showline=False,
    #             linewidth=1,
    #             tickwidth=0,
    #             gridcolor="#444",
    #             gridwidth=1
    #         ),
    #     ),
    # )
    #
    # fig = go.Figure(data=traces, layout=layout)
    # # fig = go.Figure(layout=layout)
    # fig.write_html(
    #     "retrogrades_{}.html".format(
    #         body,
    #     ),
    # )
