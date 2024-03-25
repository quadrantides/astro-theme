# coding=utf-8
"""
Created on 2020, April 16th
@author: orion
"""
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import numpy as np
import plotly.express as px
import pandas as pd
import datetime

from astro.constants import BODIES_COLORS

DATE_FORMAT = "%d/%m/%Y"

def get_body_color(body):
    return BODIES_COLORS[body]


def get_data():
    data = dict(
        year=[
            "2020",
            "2020",
            "2020",
            "2020",
        ],

        start=dict(
            date=[
                datetime.datetime(2021, 2, 17, 0, 0).strftime(format=DATE_FORMAT),
                datetime.datetime(2021, 6, 17, 0, 0).strftime(format=DATE_FORMAT),
                datetime.datetime(2021, 10, 17, 0, 0).strftime(format=DATE_FORMAT),
                datetime.datetime(2021, 2, 19, 0, 0).strftime(format=DATE_FORMAT),
            ],
            zodiac=[
                "pisces",
                "gemini",
                "sagitarius",
                "gemini",
            ],
            longitude=[
                12.0,
                12.5,
                29.1,
                14.0,
            ],
        ),

        end=dict(
            date=[
                datetime.datetime(2021, 3, 17, 0, 0).strftime(format=DATE_FORMAT),
                datetime.datetime(2021, 7, 17, 0, 0).strftime(format=DATE_FORMAT),
                datetime.datetime(2021, 11, 17, 0, 0).strftime(format=DATE_FORMAT),
                datetime.datetime(2021, 5, 19, 0, 0).strftime(format=DATE_FORMAT),
            ],
            zodiac=[
                "aquarius",
                "taurus",
                "libra",
                "gemini",
            ],
            longitude=[
                25.0,
                27.5,
                2.1,
                29.0,
            ],
        ),

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

    return data


if __name__ == '__main__':
    data = get_data()
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)
