# coding=utf-8
"""
Created on 2020, December 8th
@author: orion
"""
from transcend.models.retrogrades.revolutions.structures import \
    get_revolutions_structure as get_model_revolutions_structure

from transcend.views.charts.models.structures import get_structure as get_base_view_structure
from transcend.models.points.structures import get_polar_points_structure
from transcend.models.radius.structures import get_radii_structure
from transcend.views.charts.models.structures import get_structure as get_base_structure
from transcend.views.charts.models.lines.structures import get_line_structure


def get_structure():
    structure = get_base_view_structure()
    structure.update(
        get_model_revolutions_structure(),
    )

    return structure


def get_revolutions_structure():

    structure = get_structure()

    structure.update(
        dict(
            spiral=get_radii_structure(),
        ),
    )
    structure.update(
        get_line_structure(),
    )
    structure["line"].update(
        get_polar_points_structure(),
    )

    return structure
