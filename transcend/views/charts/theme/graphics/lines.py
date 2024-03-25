# coding=utf-8
"""
Created on 2020, April 20th
@author=orion
"""
VERSION = "1.0"


def get_all(data, legendgroup=""):
    traces = []

    for i, angle in enumerate(data['angles']):
        traces.append(
            dict(
                type="scatterpolar",
                mode='lines',
                opacity=data['opacity'],
                visible=True,
                showlegend=False,
                legendgroup=legendgroup,
                r=[
                    data['line']['radius']["min"],
                    data['line']['radius']["max"],
                ],
                theta=[
                    round(angle),
                    round(angle),
                ],
                name=data['labels'][i],
                line=dict(
                    dash=data['line']['dash'],
                    color=data['line']['color'],
                    width=data['line']['width'],
                ),
                hoverinfo='none',
            )
        )
    return traces
