# coding=utf-8
"""
Created on 2020, April 30th
@author: orion
"""
from transcend.models.points.structures import get_xy_points_structure, get_polar_points_structure
from transcend.views.charts.models.structures import get_structure as get_base_structure


def get_marker_base_structure():
    return dict(
        marker=get_base_structure(),
    )


def get_marker_structure():
    structure = get_base_structure()
    structure.update(
        dict(
            text=[],
            hovertemplate="",
            hoverinfo="",
            customdata=[],
            symbol="",
            size=0,
            color="",
            line=dict(
                color="",
                width=0,
            ),
        )
    )
    return structure


def get_polar_marker_structure():
    structure = dict(
        marker=get_marker_structure(),
    )

    structure["marker"].update(
        get_polar_points_structure(),
    )

    return structure


def get_xy_marker_structure():
    structure = dict(
        marker=get_marker_structure(),
    )

    structure["marker"].update(
        get_xy_points_structure(),
    )

    return structure
