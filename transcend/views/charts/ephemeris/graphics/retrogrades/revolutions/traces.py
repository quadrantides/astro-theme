# coding=utf-8
"""
Created on 2020, December 8th
@author=orion
"""
import numpy as np

from transcend.constants import ANGLE_OFFSET

VERSION = "1.0"


def get_polar_segment(line):

    return dict(
        type="scatterpolar",
        mode='lines',
        visible=line['visible'],
        r=line['radius'],
        theta=line['angle'],
        name=line['name'],
        showlegend=False,
        opacity=line['opacity'],
        line=dict(
            color=line['color'],
            width=line['width'],
            dash=line['dash'],
        ),
        hoverinfo=line['hoverinfo'],
    )
