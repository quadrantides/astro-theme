# coding=utf-8
"""
Created on 2020, April 28th
@author: orion
"""
from transcend.views.charts.charts import Chart

from transcend.models.planets.points.structures import get_points_structure as get_process_structure
from transcend.views.charts.models.points.structures import get_structure as get_view_structure


# PROCESS CHART


def get_process_chart(theme, chart_name, sub_chart_name=""):

    content = get_process_structure()

    return Chart(theme, chart_name, content, sub_chart_name)


# VIEW CHART


def get_view_chart(theme, chart_name, sub_chart_name=""):

    content = get_view_structure()

    return Chart(theme, chart_name, content, sub_chart_name)





# from transcend.models.planets.points.structures import get_points_structure

# from transcend.views.charts.charts import Chart
# from transcend.views.charts.models.points.structures import get_point_structure
#
# # PROCESS CHART
#
#
# def get_process_chart(theme, chart_name, sub_chart_name=""):
#
#     content = get_points_structure()
#
#     return Chart(theme, chart_name, content, sub_chart_name)
#
#
# # VIEW CHART
#
#
# def get_view_chart(theme, chart_name, sub_chart_name=""):
#
#     content = get_point_structure()
#
#     return Chart(theme, chart_name, content, sub_chart_name)
