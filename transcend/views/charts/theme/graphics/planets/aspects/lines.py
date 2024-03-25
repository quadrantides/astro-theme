# coding=utf-8
"""
Created on 2020, April 20th
@author=orion
"""
from django.utils.translation import ugettext as _

VERSION = "1.0"


def get_lines(data):
    traces = []
    aspect_type_already_shown = []

    for datai in data:

        aspect = datai['line']
        if datai['name'] in aspect_type_already_shown:
            showlegend = False
        else:
            aspect_type_already_shown.append(
                datai['name'],
            )
            showlegend = True
        traces.append(
            dict(
                type="scatterpolar",
                mode='lines',
                opacity=aspect['opacity'],
                visible=aspect['visible'],
                showlegend=showlegend,

                legendgroup=datai['name'],
                r=[
                    aspect['line']["points"]['planet1']["radius"],
                    aspect['line']["points"]['planet2']["radius"],
                ],
                theta=[
                    round(aspect['line']["points"]['planet1']["angle"]),
                    round(aspect['line']["points"]['planet2']["angle"]),
                ],
                name=aspect['line']['name'],
                line=dict(
                    dash=aspect['line']['dash'],
                    color=aspect['line']['color'],
                    width=aspect['line']['width'],
                ),
                # customdata=aspect['line']['customdata'],
                # hoverinfo='name',
                hoverinfo='none',
            )
        )

    return traces


def get_markers(data):
    traces = []
    aspect_type_already_shown = []

    for datai in data:

        marker = datai['marker']

        if datai['name'] in aspect_type_already_shown:
            showlegend = False
        else:
            aspect_type_already_shown.append(
                datai['name'],
            )
            showlegend = True

        traces.append(
            dict(
                type="scatterpolar",
                mode='markers',
                opacity=marker['opacity'],
                visible=marker['visible'],
                showlegend=showlegend,
                legendgroup=marker['name'],
                r=marker["radius"],
                theta=marker["angle"],
                name=marker['name'],
                # hovertemplate=marker['hovertemplate'],
                # customdata=marker['customdata'],
                marker=dict(
                    symbol=marker['symbol'],
                    size=marker['size'],
                    color=marker['color'],
                ),
                # # customdata=marker['marker']['customdata'],
                # hoverinfo='name',
                hoverinfo='none',
            )
        )

    return traces


def get(data):
    traces = []
    aspect_type_already_shown = []

    for datai in data:

        aspect_name = datai['name']
        if aspect_name in aspect_type_already_shown:
            showlegend = False
        else:
            aspect_type_already_shown.append(
                aspect_name,
            )
            showlegend = True

        if aspect_name == 'conjunction':
            marker = datai['marker']

            traces.append(
                dict(
                    type="scatterpolar",
                    mode='lines',
                    opacity=0.4,
                    visible=marker['visible'],
                    showlegend=showlegend,
                    # legendgroup=_(marker['name']).capitalize(),
                    r=marker["radius"],
                    theta=marker["angle"],
                    name="{}".format(_(marker['name']).capitalize()[0:5]),
                    # hovertemplate=marker['hovertemplate'],
                    # customdata=marker['customdata'],
                    marker=dict(
                        symbol=marker['symbol'],
                        size=marker['size'],
                        color=marker['color'],
                    ),
                    fill="toself",
                    fillcolor=marker['color'],
                    # # customdata=marker['marker']['customdata'],
                    # hoverinfo='name',
                    hoverinfo='none',
                )
            )
        else:
            aspect = datai['line']
            traces.append(
                dict(
                    type="scatterpolar",
                    mode='lines',
                    opacity=aspect['opacity'],
                    visible=aspect['visible'],
                    showlegend=showlegend,

                    legendgroup=datai['name'],
                    r=[
                        aspect["points"]['planet1']["radius"],
                        aspect["points"]['planet2']["radius"],
                    ],
                    theta=[
                        round(aspect["points"]['planet1']["angle"]),
                        round(aspect["points"]['planet2']["angle"]),
                    ],
                    name="{}".format(_(aspect['name']).capitalize()[0:5]),
                    line=dict(
                        dash=aspect['line']['dash'],
                        color=aspect['line']['color'],
                        width=aspect['line']['width'],
                    ),
                    # customdata=aspect['customdata'],
                    # hoverinfo='name',
                    hoverinfo='none',
                ),
            )

            if aspect_name == 'square' or aspect_name == 'trine' or aspect_name == 'sextile':
                marker = datai['marker']

                traces.append(
                    dict(
                        type="scatterpolar",
                        mode='markers',
                        opacity=marker['opacity'],
                        visible=marker['visible'],
                        showlegend=False,
                        legendgroup=_(marker['name']).capitalize(),
                        r=marker["radius"],
                        theta=marker["angle"],
                        # name=_(marker['name']).capitalize(),
                        # hovertemplate=marker['hovertemplate'],
                        # customdata=marker['customdata'],
                        marker=dict(
                            symbol=marker['symbol'],
                            size=marker['size'],
                            color=marker['color'],
                        ),
                        # # customdata=marker['marker']['customdata'],
                        # hoverinfo='name',
                        hoverinfo='none',
                    )
                )
    return traces
