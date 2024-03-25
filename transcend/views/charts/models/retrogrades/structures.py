# coding=utf-8
"""
Created on 2020, December 6th
@author: orion
"""
from transcend.models.retrogrades.structures import get_retrogrades_structure as get_model_retrogrades_structure

from transcend.views.charts.models.structures import get_structure as get_base_view_structure

from transcend.views.charts.models.annotations.structures import get_annotation_structure

from transcend.models.radius.structures import get_radii_structure

from transcend.views.charts.models.markers.structures import get_polar_marker_structure

from transcend.models.points.structures import get_polar_point_structure
from transcend.views.charts.models.structures import get_structure as get_base_structure


def get_structure():
    structure = get_base_view_structure()

    return structure


def get_retrograde_structure():

    structure = get_structure()

    # structure.update(
    #     get_radius_structure(),
    # )

    # structure.update(
    #     get_annotation_structure(),
    # )

    structure.update(
        get_polar_segment_structure(),
    )

    structure.update(
        get_polar_marker_structure(),
    )
    structure["marker"].update(
        get_radii_structure(),
    )

    return structure


def get_line_structure():

    structure = dict(
        line=dict(
            name="",
            dash='',
            color="",
            width=0,
            custom_data="",
            hover_template="",
        ),
    )
    structure["line"].update(
        get_base_structure(),
    )

    return structure


def get_polar_segment_structure():
    structure = get_line_structure()
    structure["line"].update(
        dict(
            points=dict(
                begin=get_polar_point_structure(),
                end=get_polar_point_structure(),
            ),
        ),
    )

    return structure
