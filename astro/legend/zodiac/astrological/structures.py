# coding=utf-8
"""
Created on 2020, December 19th
@author: orion
"""
from transcend.views.charts.models.structures import get_structure as get_base_structure
from transcend.views.charts.models.pie.structures import get_structure as get_pie_structure
from transcend.views.charts.models.markers.structures import get_marker_structure
from transcend.views.charts.models.segments.structures import get_polar_structure as get_polar_segment_structure


def get_structure():

    structure = get_base_structure()

    structure.update(
        get_marker_structure(),
    )

    return structure
