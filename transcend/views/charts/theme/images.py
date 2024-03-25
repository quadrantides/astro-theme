# coding=utf-8
"""
Created on 2020, March 11th
@author: orion
"""
from transcend.views.charts.theme.figure.processes import get_coordinates


def get_struct():
    return {
        "label": "",
        "source": "",
        'sizex': 0.0,
        'sizey': 0.0,
        'opacity': 1.0,
        'rmargin': 0.0,
        'xanchor': "center",
        'yanchor': "middle",
        'textposition': "center middle",
        'r': 0.0,
        'x': 0.0,
        'y': 0.0
    }


def get(angle, name, source, image):
    image['source'] = source
    image['name'] = name

    coordinates = get_coordinates(
        angle,
        image['radius'],
    )

    image.update(
        coordinates,
    )

    return image
