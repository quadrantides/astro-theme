# coding=utf-8
"""
Created on 2020, April 22th
@author=orion
"""
import numpy as np
VERSION = "1.0"


def get_points(radius):

    npoints = 500
    r = radius + np.zeros(npoints)
    theta = 360 * np.array(range(npoints)) / (npoints - 1)
    return r.tolist(), theta.tolist()


def get(aspect):
    circle = aspect['circle']
    r, theta = get_points(circle['radius'])

    return dict(
        type="scatterpolar",
        mode='lines',
        r=r,
        theta=theta,
        visible=circle['visible'],
        name=circle['name'],
        showlegend=False,
        line=dict(
            dash=circle['line']['dash'],
            width=circle['line']['width'],
            color=circle['line']['color'],
        ),
        hoverinfo='none',
    )
