# coding=utf-8
"""
Created on 2020, May 6th
@author: orion
"""


def get_rotation(values, angles):

    # plotly origin = 90° (clockwise)
    # first  sector - begin : 90° + first sector size / end : 90°
    # second sector - begin : 90° / end : 90° - second sector size
    # third sector - begin : 90° - second sector size / end : 90° - second sector size - third sector size

    return - values[0] + 90 - angles[0]

