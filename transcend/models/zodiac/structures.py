# coding=utf-8
"""
Created on 2020, May 5th
@author: orion
"""
from transcend.models.pie.structures import get_structure as get_pie_structure
VERSION = "1.0"


def get_structure(customize_values=False):

    structure = dict(
        segments=[],
        pie=get_pie_structure(),
    )

    if customize_values:
        structure.update(
            dict(
                images=[],
            ),
        )

    return structure
