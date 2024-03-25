# coding=utf-8
"""
Created on 2020, April 23th
@author=orion
"""
from django.conf import settings
VERSION = "1.0"


def get_polar_segment(line):

    dr = line['points']['external']['radius'] - line['points']['internal']['radius']

    return dict(
        type="scatterpolar",
        mode='lines',
        visible=line['visible'],
        r=[
            line['points']['internal']['radius'],
            line['points']['internal']['radius'] + 0.4 * dr,
            line['points']['external']['radius'],
        ],
        theta=[
            round(line['points']['internal']['angle']),
            round(line['points']['internal']['angle']),
            round(line['points']['external']['angle']),
        ],
        name=line['name'],
        showlegend=False,
        opacity=line['opacity'],
        line=dict(
            color=line['color'],
            width=line['width'],
            dash=line['dash'],
        ),
        hoverinfo='none',
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
        hoverdistance=100,
    )


def get_polar_marker(marker):

    return dict(

        type="scatterpolar",
        mode='markers',
        visible=marker['visible'],
        r=[marker['radius']],
        theta=[marker['angle']],
        text=[marker['text']],
        name=marker['name'],
        showlegend=False,
        # hovertemplate=marker['hovertemplate'],
        # customdata=marker['customdata'],
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
