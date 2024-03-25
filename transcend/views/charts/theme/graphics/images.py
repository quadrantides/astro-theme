# coding=utf-8
"""
Created on 2020, April 22th
@author=orion
"""
VERSION = "1.0"


def get_one(data, visible=None):
    if not visible:
        if 'visible' in data.keys():
            visible = data['visible']
        else:
            visible = True

    if data['name']:
        name = data['name']
    else:
        name = ""

    return dict(
        x=data['x'],
        y=data['y'],
        name=name,
        visible=visible,
        sizex=data['sizex'],
        sizey=data['sizey'],
        source=data['source'],
        xanchor=data['xanchor'],
        yanchor=data['yanchor'],
        layer=data['layer'],
        # xref="paper",
        # yref="paper",
        # xref="x",
        # yref="y",
        opacity=data['opacity'],
        # hovertemplate=data['hovertemplate'],
    )


def get_all(data):
    res = []

    for item in data:
        res.append(
            get_one(item),
        )
    return res
