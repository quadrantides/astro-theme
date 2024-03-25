# coding=utf-8
"""
Created on 2020, April 26th
@author: orion
"""
from transcend.models.planets.structures import get_structure as get_model_base_point_structure

from transcend.views.charts.models.structures import get_structure as get_base_structure
from transcend.views.charts.models.annotations.structures import get_annotation_with_arrow_structure
from transcend.views.charts.models.segments.structures import get_polar_structure as get_polar_segment_structure


def get_structure():

    structure = get_base_structure()
    structure.update(
        get_model_base_point_structure(),
    )

    structure.update(
        get_annotation_with_arrow_structure(),
    )

    structure.update(
        get_polar_segment_structure(),
    )

    return structure
