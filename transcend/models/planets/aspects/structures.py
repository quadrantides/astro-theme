# coding=utf-8
"""
Created on 2020, April 17th
@author: orion
"""
VERSION = "1.0"


def get_type_structure():
    return dict(
        degree=0,
        name='',
        color='',
        visible=0,
        visible_grid=0,
        is_major=0,
        is_minor=0,
        orb='',
    )


def get_aspect_structure():
    return dict(
        aspect=dict(
            planets=[],
            type=get_type_structure(),
        )
    )


def get_aspects_structure():
    return dict(
        aspects=[],
    )
