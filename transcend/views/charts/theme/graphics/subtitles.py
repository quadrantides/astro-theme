# coding=utf-8
"""
Created on 2020, April 22th
@author=orion
"""
VERSION = "1.0"


def get(x, y, text):

    textfontsize = 11

    return dict(
        x=x,
        y=y,
        text=text,
        font=dict(
            color="black",
            size=textfontsize,
        ),
        showarrow=False,
        xref="paper",
        yref="paper",
        xanchor="left",
        yanchor="middle",
    )
