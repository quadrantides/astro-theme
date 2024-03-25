# coding=utf-8
"""
Created on 2020, December 19th
@author=orion
"""
VERSION = "1.0"


def get_text(data):

    return dict(
        type="scatter",
        mode='text',
        visible=data['visible'],
        x=data['x'],
        y=data['y'],
        text=data['text'],
        name=data['name'],
        showlegend=False,
        opacity=data['opacity'],
        hoverinfo="none",
    )
