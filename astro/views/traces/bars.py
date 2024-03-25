# coding=utf-8
"""
Created on 2020, December 18th
@author=orion
"""
VERSION = "1.0"


def get_shape(bar):
    return dict(
        type="rect",
        visible=bar['visible'],
        opacity=bar['opacity'],
        name=bar['name'],
        x0=bar['x0'],
        y0=bar['y0'],
        x1=bar['x1'],
        y1=bar['y1'],
        fillcolor=bar['fillcolor'],
        layer=bar['layer'],
        xref="x", yref="y",
        line=dict(
            color=bar['line']['color'],
            width=0,
        ),
        # hoverinfo='none',
    )

# def get_bar(bar):
#     return dict(
#         type="scatter",
#         mode="lines",
#         visible=bar['visible'],
#         opacity=bar['opacity'],
#         name=bar['name'],
#         # orientation=bar['orientation'],
#         x=bar['x'],
#         y=bar['y'],
#         fill="toself",
#         # width=bar['width'],
#         # layer=bar['layer'],
#         marker=dict(
#             color=bar['marker']['color'],
#             line=dict(
#                 color=bar['marker']['line']['color'],
#                 width=bar['marker']['line']['width'],
#             )
#         ),
#         hoverinfo='none',
#     )
