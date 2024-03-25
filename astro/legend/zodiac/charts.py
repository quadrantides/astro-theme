# coding=utf-8
"""
Created on 2020, December 16th
@author: orion
"""
from transcend.views.charts.charts import Chart

from astro.models.legend.zodiac.structures import get_structure as get_zodiac_process_structure
from astro.legend.zodiac.structures import get_structure as get_zodiac_view_structure


# PROCESS CHART


def get_process_chart():

    content = get_zodiac_process_structure()

    return Chart("legend", "positions", content, "")


# VIEW CHART


def get_view_chart(zodiac_type):

    content = get_zodiac_view_structure()

    return Chart("legend", zodiac_type, content, "")
