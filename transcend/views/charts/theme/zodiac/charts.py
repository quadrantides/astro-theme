# coding=utf-8
"""
Created on 2020, April 26th
@author: orion
"""
from transcend.views.charts.charts import Chart

from transcend.models.zodiac.structures import get_structure as get_zodiac_process_structure
from transcend.views.charts.models.zodiac.structures import get_structure as get_zodiac_view_structure


# PROCESS CHART


def get_process_chart(theme, chart_name, sub_chart_name="", customize_values=False):

    content = get_zodiac_process_structure(customize_values=customize_values)

    return Chart(theme, chart_name, content, sub_chart_name)


# VIEW CHART


def get_view_chart(theme, chart_name, sub_chart_name="", customize_values=False):

    content = get_zodiac_view_structure(customize_values=customize_values)

    return Chart(theme, chart_name, content, sub_chart_name)
