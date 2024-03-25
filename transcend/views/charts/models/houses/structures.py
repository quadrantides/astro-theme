# coding=utf-8
"""
Created on 2020, April 26th
@author: orion
"""
from transcend.views.charts.models.structures import get_structure as get_base_structure
from transcend.views.charts.models.pie.structures import get_structure as get_pie_structure
from transcend.views.charts.models.segments.structures import get_polar_structure as get_polar_segment_structure
from transcend.views.charts.models.annotations.structures import get_annotation_structure


def get_structure():
    structure = get_base_structure()

    structure.update(
        get_pie_structure(),
    )

    structure.update(
        get_annotation_structure(),
    )

    structure.update(
        get_polar_segment_structure(),
    )

    return structure
