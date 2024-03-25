# coding=utf-8
"""
Created on 2020, April 27th
@author: orion
"""
from transcend.views.charts.charts import Chart

from transcend.views.charts.models.structures import get_structure as get_base_structure
from transcend.views.charts.models.lines.structures import get_line_structure
from transcend.models.radius.structures import get_radius_structure


# PROCESS CHART


def get_process_chart(theme, chart_name, sub_chart_name=""):

    content = get_radius_structure()

    return Chart(theme, chart_name, content, sub_chart_name)


# VIEW CHART


def get_view_chart(theme, chart_name, sub_chart_name=""):

    content = get_base_structure()

    content.update(
        get_radius_structure(),
    )

    content.update(
        get_line_structure(),
    )

    return Chart(theme, chart_name, content, sub_chart_name)
