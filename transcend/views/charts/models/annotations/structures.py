# coding=utf-8
"""
Created on 2020, April 26th
@author: orion
"""
from transcend.views.charts.models.structures import get_structure as get_base_structure


def get_annotation_structure():
    structure = dict(
        annotation=dict(
            text="",
            x=0.0,
            y=0.0,
            radius=0.0,
            angle=0.0,
            xanchor="",
            yanchor="",
            textposition="",
            font=dict(
                color="",
                size=0,
            ),
        ),
    )
    structure["annotation"].update(
        get_base_structure(),
    )
    return structure


def get_annotation_with_arrow_structure():
    structure = get_annotation_structure()
    structure["annotation"].update(
        dict(
            arrowcolor="",
            showarrow=True,
            showtext=True,
            ax=0.0,
            ay=0.0,
            xshift=0.0,
            yshift=0.0,
        ),
    )
    return structure
