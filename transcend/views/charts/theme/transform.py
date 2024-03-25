# coding=utf-8
"""
Created on 2020, April 27th
@author: orion
"""
from transcend.views.charts.theme.constants import WHEEL

SCALE_FACTOR = WHEEL['layout']["polar"]["domain"]["x"][1] * WHEEL['layout']["xaxis"]["range"][1]


def get_layout_size():
    return WHEEL['layout']["width"]


def get_polar_plot_size():
    return SCALE_FACTOR * get_layout_size()


def get_radius_in_polar_coords(radius):
    return radius / get_polar_plot_size()


def get_radius_in_xy_coords(radius):
    return radius * WHEEL['layout']["polar"]["domain"]["x"][1] / get_layout_size()
