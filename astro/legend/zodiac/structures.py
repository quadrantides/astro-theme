# coding=utf-8
"""
Created on 2020, May 5th
@author: orion
"""
from transcend.views.charts.models.structures import get_structure as get_base_structure
from transcend.views.charts.models.pie.structures import get_structure as get_pie_structure
from transcend.views.charts.models.images.structures import get_structure as get_image_structure
from transcend.views.charts.models.segments.structures import get_polar_structure as get_polar_segment_structure


def get_structure(customize_values=False):

    structure = get_base_structure()

    structure.update(
        get_pie_structure(),
    )

    structure.update(
        dict(
            segment=get_polar_segment_structure(),
        ),
    )

    structure["segment"].update(
        dict(
            ticks=dict(
                dtick=0.0,
            ),
        ),
    )

    if customize_values:
        structure.update(
            get_image_structure(),
        )
    return structure
