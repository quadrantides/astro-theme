# coding=utf-8
"""
Created on 2020, May 1st
@author: orion
"""
from transcend.models.points.structures import get_polar_point_structure, get_xy_point_structure
from transcend.views.charts.models.structures import get_structure as get_base_structure

from transcend.views.charts.models.lines.structures import get_line_structure as get_base_line_structure


def get_xy_structure():
    structure = get_base_line_structure()
    structure.update(
        dict(
            points=dict(
                internal=get_xy_point_structure(),
                external=get_xy_point_structure(),
            ),
        ),
    )

    structure.update(
        get_base_structure(),
    )

    return structure


def get_polar_structure():
    structure = get_base_line_structure()
    structure['line'].update(
        dict(
            points=dict(
                internal=get_polar_point_structure(),
                external=get_polar_point_structure(),
            ),
        ),
    )

    structure['line'].update(
        get_base_structure(),
    )

    return structure
