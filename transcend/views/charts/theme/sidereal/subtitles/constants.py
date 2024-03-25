# coding=utf-8
"""
Created on 2020, April 21th
@author: orion
"""
import copy
from transcend.views.charts.theme.tropical.subtitles.constants import get_structure as get_base_structure

VERSION = "1.0"


def get_structure():
    structure = copy.deepcopy(
        get_base_structure(),
    )
    structure["chart"]['theme']["titles"]['position']["top"]['left']['mode'] = dict()
    return structure
