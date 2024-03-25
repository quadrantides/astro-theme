# coding=utf-8
"""
Created on 2020, December 14th
@author: orion
"""
from transcend.views.charts.charts import Chart

from transcend.models.retrogrades.structures import get_retrogrades_structure as get_process_structure
from transcend.views.charts.models.retrogrades.structures import get_structure as get_view_structure


# PROCESS CHART


def get_process_chart():

    content = get_process_structure()

    return Chart("ephemeris", "positions", content, "")


# VIEW CHART


def get_view_chart():

    content = get_view_structure()

    return Chart("ephemeris", "positions", content, "")
