# coding=utf-8
"""
Created on 2020, March 28th
@author: orion
"""
from transcend.models.planets.aspects.structures import get_aspect_structure


VERSION = "1.0"


ASPECT_LEGEND_STRUCTURE = {

    'chart': {
        'aspect': {
            'legend': {},
        }
    },
}

ASPECT_LEGEND_STRUCTURE['chart']['aspect']['legend'].update(
    get_aspect_structure()['aspect'],
)

ASPECT_LEGEND_STRUCTURE['chart']['aspect']['legend'].update(
    {
        'visible': True,
        'radius': 0.0,
        'line': {
            'color': "",
            'width': 0,
        },
    },
)

LEGEND_STRUCTURE = {

    'chart': {
        'aspects': {
            'legend': {
                "tropical": [],
                'sidereal': [],
            }
        },
    },
}