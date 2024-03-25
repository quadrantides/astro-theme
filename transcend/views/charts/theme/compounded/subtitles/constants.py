# coding=utf-8
"""
Created on 2020, April 18th
@author: orion
"""
import copy
from transcend.views.charts.theme.subtitles.constants import TITLES as BASE_TITLES

VERSION = "1.0"


def get_structure():

    structrure = copy.deepcopy(
        BASE_TITLES,
    )

    structrure["chart"]['theme']["titles"]['position']["bottom"] = dict()

    structrure["chart"]['theme']["titles"]['position']["bottom"]['left'] = dict()
    structrure["chart"]['theme']["titles"]['position']["bottom"]['left']['tropical title'] = dict()
    structrure["chart"]['theme']["titles"]['position']["bottom"]['left']['tropical houses_system'] = dict()

    structrure["chart"]['theme']["titles"]['position']["bottom"]['right'] = dict()
    structrure["chart"]['theme']["titles"]['position']["bottom"]['right']['sidereal title'] = dict()
    structrure["chart"]['theme']["titles"]['position']["bottom"]['right']['sidereal houses_system'] = dict()
    structrure["chart"]['theme']["titles"]['position']["bottom"]['right']['sidereal mode'] = dict()
    return structrure
