# coding=utf-8
"""
Created on 2020, April 23th
@author=orion
"""
import numpy as np

from transcend.constants import ANGLE_OFFSET

VERSION = "1.0"


def get_polar_segment(line):

    # dtheta = line['points']['begin']['angle'] - line['points']['end']['angle']
    # theta0 = line['points']['end']['angle']

    nb_points = len(line['theta'])
    # nb_degrees = int(dtheta)

    # theta = ANGLE_OFFSET + theta0 + nb_degrees * np.array(list(range(nb_degrees))) / (nb_degrees - 1)

    # r = [line['points']['begin']['radius']] * nb_degrees
    customdata = line['custom_data'] * nb_points

    return dict(
        type="scatterpolar",
        mode='lines',
        visible=line['visible'],
        text=line['text'],
        r=line['r'],
        theta=line['theta'],
        name=line['name'],
        showlegend=False,
        opacity=line['opacity'],
        line=dict(
            color=line['color'],
            width=line['width'],
            dash=line['dash'],
        ),
        customdata=customdata,
        # hovertemplate=line['hover_template'],
        hoverinfo='text',
    )


def get_xy_marker(data):

    return dict(

        type="scatter",
        mode='markers',
        visible=data['visible'],
        x=[data['x']],
        y=[data['y']],
        text=[data['text']],
        name=data['name'],
        showlegend=False,
        # hovertemplate=data['hovertemplate'],
        # customdata=data['customdata'],
        opacity=data['opacity'],
        marker=dict(
            symbol=data['marker']['symbol'],
            size=data['marker']['size'],
            color=data['marker']['color'],
        ),
        hoverinfo='none',
    )


def get_polar_marker(marker):
    marker['opacity'] = 0.5
    marker['color'] = "#ddd"
    marker['line']['color'] = marker['color']
    marker['symbol'] = "circle"
    return dict(

        type="scatterpolar",
        mode='lines',
        visible=marker['visible'],
        r=marker['radius'],
        theta=marker['angle'],
        showlegend=False,
        opacity=marker['opacity'],
        marker=dict(
            symbol=marker['symbol'],
            size=marker['size'],
            color=marker['color'],
            line=dict(
                color=marker['line']['color'],
                width=marker['line']['width'],
            ),
        ),
        hoverinfo='none',
    )
