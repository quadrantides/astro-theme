# coding=utf-8
"""
Created on 2020, April 16th
@author: orion
"""
"""
    WHEEL DIMENSIONS
"""

WIDTH_PX = 1100
HEIGHT_PX = 650


DIMENSIONS = {
    'layout': dict(
        width=WIDTH_PX,
        height=HEIGHT_PX,
        xaxis=dict(
            range=[0, 360],
        ),
        yaxis=dict(
            range=[0, 360],
        ),
    ),
    'width': WIDTH_PX,
    'height': HEIGHT_PX,
}


blue = "#668cff"
green = "#33cc33"
brown = "#bf8040"
red = "#ff1a1a"

COLORS = dict(
    aries=red,
    taurus=green,
    gemini=brown,
    cancer=blue,
    leo=red,
    virgo=green,
    libra=brown,
    scorpio=blue,
    sagittarius=red,
    capricorn=green,
    aquarius=brown,
    pisces=blue,
)