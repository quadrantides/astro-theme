# coding=utf-8
"""
Created on 2020, April 30th
@author: orion
"""
from transcend.models.points.structures import get_polar_point_structure
from transcend.models.radius.structures import get_radius_structure

from transcend.views.charts.models.structures import get_structure as get_base_structure
from transcend.views.charts.models.lines.structures import get_line_structure
from transcend.views.charts.models.markers.structures import get_polar_marker_structure


def get_circle_structure():

    structure = get_base_structure()
    structure.update(
        get_radius_structure()
    )

    structure.update(
        get_line_structure(),
    )

    return structure


def get_segment_structure():

    structure = get_base_structure()
    structure.update(
        get_radius_structure()
    )

    structure.update(
        get_line_structure(),
    )

    return structure


def get_aspect_line_structure():
    structure = dict(
        line=get_line_structure(),
    )

    structure['line'].update(
        dict(
            customdata=[],
            points=dict(
                planet1=get_polar_point_structure(),
                planet2=get_polar_point_structure(),
            ),
        ),
    )

    return structure


def get_structure():

    content = get_base_structure()

    content.update(
        dict(
            circle=get_circle_structure(),
        )
    )

    content.update(
        get_aspect_line_structure(),
    )

    content.update(
        get_polar_marker_structure(),
    )

    return content
