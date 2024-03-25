# coding=utf-8
"""
Created on 2020, April 23th
@author=orion
"""
VERSION = "1.0"


def get(data):
    return \
        dict(
            opacity=data['opacity'],
            x=data['x'],
            y=data['y'],
            text=data['text'],
            font=dict(
                color=data['font']['color'],
                size=data['font']['size'],
                family=data['font']['family'],
            ),
            showarrow=False,
            xref="x",
            yref="y",
            xanchor=data['xanchor'],
            yanchor=data['yanchor'],
        )
