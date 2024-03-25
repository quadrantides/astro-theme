# coding=utf-8
"""
Created on 2020, April 26th
@author: orion
"""
from transcend.views.charts.charts import Chart

# PROCESS CHART


def get_process_chart(theme, chart_name, content, sub_chart_name=""):

    return Chart(theme, chart_name, content, sub_chart_name)
