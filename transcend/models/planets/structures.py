# coding=utf-8
"""
Created on 2020, April 14th
@author: orion
"""
VERSION = "1.0"


def get_structure():
    return dict(
        label="",
        angle=0.0,
    )


def get_planets_structure():
    return dict(
        planets=[],
        transit_planets=[],
    )
