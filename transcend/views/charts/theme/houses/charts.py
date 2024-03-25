# coding=utf-8
"""
Created on 2020, April 26th
@author: orion
"""
from transcend.models.houses.structures import get_structure as get_process_structure
from transcend.views.charts.models.houses.structures import get_structure as get_view_structure

from transcend.views.charts.charts import Chart

# PROCESS CHART


def get_process_chart(theme, chart_name, sub_chart_name=""):

    content = get_process_structure()

    return Chart(theme, chart_name, content, sub_chart_name)


# VIEW CHART


def get_view_chart(theme, chart_name, sub_chart_name=""):

    structure = get_view_structure()

    return Chart(theme, chart_name, structure, sub_chart_name)
