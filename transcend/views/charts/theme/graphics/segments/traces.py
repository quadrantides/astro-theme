# coding=utf-8
"""
Created on 2020, May 1st
@author=orion
"""
VERSION = "1.0"


def get_polar_segment(line):

    return dict(
        type="scatterpolar",
        mode='lines',
        visible=line['visible'],
        r=[
            line['points']['internal']['radius'],
            line['points']['external']['radius'],
        ],
        theta=[
            int(round(line['points']['internal']['angle'])),
            int(round(line['points']['external']['angle'])),
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


def get_xy_segment(line):

    return dict(
        type="scatter",
        mode='lines',
        visible=line['visible'],
        x=[
            line['points']['internal']['x'],
            line['points']['external']['x'],
        ],
        y=[
            line['points']['internal']['y'],
            line['points']['external']['y'],
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


def get_lines(annotations):
    traces = []
    for annotation in annotations:
        traces.append(
            get_xy_segment(annotation['line']),
        )
    return traces


def get_polar_segments(data):
    traces = []
    for datai in data:
        traces.append(
            get_polar_segment(datai['line']),
        )
    return traces
