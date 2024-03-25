# coding=utf-8
"""
Created on 2020, April 23th
@author=orion
"""
VERSION = "1.0"


def get_line(point, opposites=False, legendgroup=""):

    rotation = 180 if opposites else 0

    return dict(
        type="scatterpolar",
        mode='lines',
        visible=point['visible'],
        opacity=point['opacity'],
        name=point['name'],
        showlegend=False,
        legendgroup=legendgroup,
        r=[
            point['line']["points"]['internal']['radius'],
            point['line']["points"]['external']['radius'],
        ],
        theta=[
            round(point['line']["points"]['internal']['angle']) + rotation,
            round(point['line']["points"]['internal']['angle']) + rotation,
        ],
        line=dict(
            dash=point['line']['dash'],
            color=point['line']['color'],
            width=point['line']['width'],
        ),
        hoverinfo='none',
    )


def get_all(data):
    traces = []

    for point in data:
        traces.append(
            get_line(point),
        )
        traces.append(
            get_line(point, opposites=True),
        )
    return traces
