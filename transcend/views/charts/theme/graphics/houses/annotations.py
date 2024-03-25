# coding=utf-8
"""
Created on 2020, April 23th
@author=orion
"""
VERSION = "1.0"


def get_all(data):
    res = []

    annotations = data['annotations']
    for annotation in annotations:
        res.append(
            dict(
                opacity=data['opacity'],
                x=annotation['annotation']['x'],
                y=annotation['annotation']['y'],
                text=annotation['annotation']['label'],
                font=dict(
                    color=annotation['annotation']['font']['color'],
                    size=annotation['annotation']['font']['size'],
                ),
                showarrow=False,
                xref="x",
                yref="y",
                xanchor=annotation['annotation']['xanchor'],
                yanchor=annotation['annotation']['yanchor'],
            )
        )
    return res
