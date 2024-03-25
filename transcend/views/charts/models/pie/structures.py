# coding=utf-8
"""
Created on 2020, April 26th
@author: orion
"""
from transcend.views.charts.models.structures import get_structure as get_base_structure


def get_structure():

    structure = dict(
        pie=dict(
            get_base_structure(),
        ),
    )
    structure["pie"].update(
        dict(
            domain=dict(
                x=[],
                y=[],
            ),
            colors=[],
            hole=0.0,
            textinfo=None,
            hovertext='',
            hoverinfo='',
            hovertemplate="",
            customdata=[],
            marker=dict(
                colors=[],
                line=dict(
                    width=0.0,
                    color="",
                ),
            ),
        ),
    )
    return structure
