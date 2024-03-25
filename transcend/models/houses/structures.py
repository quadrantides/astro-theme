# coding=utf-8
"""
Created on 2020, May 1st
@author: orion
"""
from transcend.models.radius.structures import get_radii_structure
from transcend.models.pie.structures import get_structure as get_pie_structure

VERSION = "1.0"


def get_structure():

    structure = dict(
        pie=get_pie_structure(),
        angles=[],
        labels=[],
    )

    structure.update(
        get_radii_structure(),
    )

    structure.update(
        dict(annotations=[]),
    )

    return structure
