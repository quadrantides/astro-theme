# coding=utf-8
"""
Created on 2020, March 18th
@author: orion
"""
from transcend.models.planets.aspects.structures import get_aspect_structure
VERSION = "1.0"

COLORS = {
    'conjunction': "#00ff00",
    'semi-sextile': "#810757",
    'semi-square': "#b14e58",
    'sextile': "#0000ff",
    'quintile': "#1f99b3",
    'square': "#ff0000",
    'trine': "#0000ff",
    'sesquiquadrate': "#985a10",
    'biquintile': "#7a9810",
    'quincunx': "#00802b",
    'opposition': "#ff0000",
}

ASPECT_STRUCTURE = {

    'chart': {
    },
}

ASPECT_STRUCTURE['chart'].update(
    get_aspect_structure(),
)

ASPECT_STRUCTURE['chart']['aspect'].update(
    {
        'visible': True,
        'radius': 0.0,
        'line': {
            'color': "",
            'width': 0,
        },
    },
)

ASPECTS_STRUCTURE = {

    'chart': {
        'aspects': {
            "tropical": [],
            'sidereal': [],
        },
    },
}
