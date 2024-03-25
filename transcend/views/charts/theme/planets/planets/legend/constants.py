# coding=utf-8
"""
Created on 2020, March 27th
@author: orion
"""
import copy

VERSION = "1.0"

PLANETS = ['sun', 'mercury', 'venus', 'moon', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto', 'chiron', 'mean apogee']

POSITIONS = {
    'sun': 0,
    'mercury': 1,
    'venus': 2,
    'moon': 3,
    'mars': 4,
    'jupiter': 5,
    'saturn': 6,
    'uranus': 7,
    'neptune': 8,
    'pluto': 9,
    'chiron': 10,
}


def get_angles():
    res = dict()
    nplanets = len(PLANETS)
    for i, planet in enumerate(PLANETS):
        res[planet] = {'angle': i * 360 / nplanets}

    return res


def get_text_position(angle):
    yanchor = "top"
    xanchor = "right"
    if angle <= 15 or angle > 315:
        yanchor = "top"
        xanchor = "right"
    elif 15 < angle <= 135:
        xanchor = "right"
        yanchor = "bottom"
    elif 135 < angle <= 225:
        yanchor = "bottom"
        xanchor = "right"
    elif 225 < angle <= 315:
        yanchor = "bottom"
        xanchor = "right"

    return '{} {}'.format(xanchor, yanchor)


def get_image_arguments(angle, chart_definition):

    res = copy.deepcopy(chart_definition)
    textposition = get_text_position(angle)

    res['textposition'] = textposition

    return res


PLANET_LEGEND_STRUCTURE = {

    'chart': {
        'planet': {
            'legend': {
                "label": "",
                "visible": "",
                "angle": 0.0,
                "image": dict(),
                "text": {
                    "position": "",
                },
            },
        },
    },
}

LEGEND_STRUCTURE = {

    'chart': {
        'planets': {
            'legend': []
        },
    },
}
