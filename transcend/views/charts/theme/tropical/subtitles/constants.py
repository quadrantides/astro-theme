# coding=utf-8
"""
Created on 2020, April 21th
@author: orion
"""
import copy
from transcend.views.charts.theme.subtitles.constants import TITLES as BASE_TITLES

VERSION = "1.0"


def get_structure():

    structure = copy.deepcopy(
        BASE_TITLES,
    )

    structure["chart"]['theme']["titles"]['position']["top"]['left']['houses_system'] = dict()
    return structure

