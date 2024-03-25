# coding=utf-8
"""
Created on 2020, April 26th
@author: orion
"""
from transcend.views.charts.models.structures import get_structure as get_base_structure


def get_line_structure():

    structure = get_base_structure()
    structure.update(
        dict(
            line=dict(
                name="",
                dash='',
                color="",
                width=0,
            ),
        ),
    )
    return structure


def get_line_maker_structure():

    structure = get_base_structure()
    structure.update(
        dict(
            line=dict(
                name="",
                dash='',
                color="",
                width=0,
            ),
        ),
    )
    return structure
