# coding=utf-8
"""
Created on 2020, December 17th
@author: orion
"""
from transcend.views.charts.models.structures import get_structure as get_base_view_structure
from transcend.views.charts.models.markers.structures import get_xy_marker_structure


def get_structure():
    structure = get_base_view_structure()
    return structure


def get_position_structure():

    structure = get_structure()

    structure.update(
        get_xy_marker_structure(),
    )

    return structure
