# coding=utf-8
"""
Created on 2020, December 17th
@author=orion
"""
VERSION = "1.0"


def get_segment(marker):

    return dict(
        type="scattergl",
        mode='markers',
        visible=marker['visible'],
        x=marker['x'],
        y=marker['y'],
        name=marker['name'],
        showlegend=marker['show_legend'],
        legendgroup=marker['name'],
        opacity=marker['opacity'],
        marker=dict(
            symbol=marker['symbol'],
            size=marker['size'],
            color=marker['color'],
        ),
        hovertemplate=marker['hovertemplate'],
        customdata=marker['custom_data'],
    )
