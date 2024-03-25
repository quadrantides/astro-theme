# coding=utf-8
"""
Created on 2020, April 23th
@author=orion
"""

VERSION = "1.0"


def get(data, textangle):

    annotation = data["annotation"]

    return dict(
        visible=data['visible'],
        opacity=data['opacity'],
        name=data['name'],
        x=annotation['x'],
        y=annotation['y'],
        text=annotation["text"],
        font=dict(
            color=annotation["font"]["color"],
            size=annotation["font"]["size"],
        ),
        showarrow=annotation["showarrow"],
        arrowcolor=annotation["arrowcolor"],
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        # startarrowsize=4,
        textangle=textangle,
        xshift=annotation['xshift'],
        yshift=annotation['yshift'],
        ax=annotation['ax'],
        ay=annotation['ay'],
        xanchor=annotation['xanchor'],
        yanchor=annotation['yanchor'],
        xref="x",
        yref="y",
    )


def get_angle(data, textangle):

    annotation = data["annotation"]

    return dict(
        visible=data['visible'],
        opacity=data['opacity'],
        name=data['name'],
        x=annotation['x'],
        y=annotation['y'],
        text=annotation["text"],
        font=dict(
            color=annotation["font"]["color"],
            size=10,
        ),
        showarrow=annotation["showarrow"],
    )


def get_all(data):
    annotations = []
    textangle = 0
    for point in data:
        annotations.append(
            get(point, textangle)
        )
        # annotations.append(
        #     get(point[0], textangle)
        # )
        # annotations.append(
        #     get_angle(point[1], textangle)
        # )
    return annotations
