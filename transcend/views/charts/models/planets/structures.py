# coding=utf-8
"""
Created on 2020, April 26th
@author: orion
"""
from transcend.models.planets.structures import get_structure as get_model_planet_structure

from transcend.views.charts.models.structures import get_structure as get_base_view_structure

from transcend.views.charts.models.annotations.structures import get_annotation_structure
from transcend.views.charts.models.images.structures import get_structure
from transcend.models.radius.structures import get_radius_structure
# from transcend.views.charts.models.markers.structures import get_xy_marker_structure

from transcend.views.charts.models.segments.structures import get_polar_structure as get_polar_segment_structure
from transcend.views.charts.models.pie.structures import get_structure as get_pie_structure
from transcend.views.charts.models.markers.structures import get_polar_marker_structure
from transcend.views.charts.models.images.structures import get_structure as get_image_structure


def get_structure():
    structure = get_base_view_structure()
    structure.update(
        get_model_planet_structure(),
    )

    return structure


def get_planet_structure():

    structure = get_structure()

    structure.update(
        get_radius_structure(),
    )

    structure.update(
        dict(
            box_size=0,
        ),
    )
    structure.update(
        get_annotation_structure(),
    )

    # structure.update(
    #     get_xy_marker_structure(),
    # )

    # structure.update(
    #     get_pie_structure(),
    # )

    structure.update(
        get_polar_segment_structure(),
    )

    structure.update(
        get_polar_marker_structure(),
    )
    structure["marker"].update(
        get_radius_structure(),
    )

    structure.update(
        get_image_structure(),
    )

    return structure
