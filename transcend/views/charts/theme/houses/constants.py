# coding=utf-8
"""
Created on 2020, April 13th
@author: orion
"""
from transcend.models.houses.constants import STRUCTURE as MODEL_STRUCTURE

VERSION = "1.0"

COLORS = [
    "#eee", "#fff",
    "#eee", "#fff",
    "#eee", "#fff",
    "#eee", "#fff",
    "#eee", "#fff",
    "#eee", "#fff",
]


def get_radius_structure():
    return {
            'radius': {
                'min': 0.0,
                'max': 0.0,
            },
        }


def get_annotation_structure():

    return dict(
        x=0.0,
        y=0.0,
        label="",
        xanchor="",
        yanchor="",
    )


def get_annotations_structure():

    return dict(annotations=[])


def get_structure(chart_name):

    structure = {"chart": {
            chart_name: {
                'houses': dict()
            },
        }
    }

    structure['chart'][chart_name]['houses'].update(
        MODEL_STRUCTURE['houses'],
    )

    structure['chart'][chart_name]['houses'].update(
        get_radius_structure(),
    )

    structure['chart'][chart_name]['houses'].update(
        get_annotations_structure(),
    )

    return structure
