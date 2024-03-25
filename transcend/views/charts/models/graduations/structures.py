# coding=utf-8
"""
Created on 2020, May 6th
@author: orion
"""
from transcend.views.charts.models.structures import get_structure as get_base_structure

from transcend.views.charts.models.lines.structures import get_line_structure
from transcend.views.charts.models.ticks.structures import get_ticks_structure
from transcend.models.radius.structures import get_radii_structure


def get_structure():

    structure = get_base_structure()

    structure.update(
        get_radii_structure(),
    )

    structure.update(
        get_line_structure(),
    )

    structure.update(
        get_ticks_structure(),
    )

    return structure
