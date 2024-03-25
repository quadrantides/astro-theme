# coding=utf-8
"""
Created on 2020, April 26th
@author: orion
"""
from transcend.views.charts.models.structures import get_structure as get_base_structure


def get_structure():
    structure = dict(
        image=dict(
            name="",
            label="",
            x=0.0,
            y=0.0,
            radius=0.0,
            angle=0.0,
            sizex=0.0,
            sizey=0.0,
            xanchor="",
            yanchor="",
            opacity=0.0,
            source="",
            layer="",
            hovertemplate="",
        )
    )
    structure['image'].update(
        get_base_structure(),
    )

    return structure
