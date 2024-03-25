# coding=utf-8
"""
Created on 2020, April 14th
@author: orion
"""
from transcend.models.pie.structures import get_structure as get_process_pie_structure

VERSION = "1.0"


def get_planets_structure():

    structure = dict(
        planets=[],
    )
    # structure.update(
    #     get_process_pie_structure(),
    # )

    return structure
