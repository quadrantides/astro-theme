# coding=utf-8
"""
Created on 2020, May 5th
@author=orion
"""
VERSION = "1.0"


def get_pie(data):
    labels = []
    for label in data['labels']:
        if len(label) > 6:
            label = label[0:6] + "."
        labels.append(
            label,
        )
    if data['textinfo']:
        trace = dict(
            type='pie',
            hole=data['hole'],
            labels=labels,
            values=data['values'],
            name=data['name'],
            rotation=data['rotation'],
            sort=False,
            opacity=data['opacity'],
            marker=dict(
                colors=data['colors'],
                line=dict(
                    color=data['marker']['line']['color'],
                    width=data['marker']['line']['width'],
                ),
            ),
            showlegend=False,
            domain=data['domain'],
            # text=data['text'],
            textinfo=data['textinfo'],
            # hoverinfo='label+text',
            # hovertext=data['hovertext'],
            # hovertemplate=data['hovertemplate'],
            # customdata=data['customdata'],
            insidetextorientation='tangential',
            insidetextfont=dict(
                color='black',
                size=10,
            ),
            # hoverinfo=data['hoverinfo'],
            hoverinfo='none',
        )
    else:
        trace = dict(
            type='pie',
            hole=data['hole'],
            labels=labels,
            values=data['values'],
            name=data['name'],
            rotation=data['rotation'],
            sort=False,
            opacity=data['opacity'],
            marker=dict(
                colors=data['colors'],
                line=dict(
                    color=data['marker']['line']['color'],
                    width=data['marker']['line']['width'],
                ),
            ),
            showlegend=False,
            domain=data['domain'],
            # text=data['text'],
            textinfo=data['textinfo'],
            # hovertext=data['hovertext'],
            # hoverinfo=data['hoverinfo'],
            # hovertemplate=data['hovertemplate'],
            # customdata=data['customdata'],
            hoverinfo='none',
        )

    return trace


def get_ticks(segments):

    traces = []

    for segment in segments:
        dtick = segment["ticks"]['dtick']
        if segment["points"]['internal']['angle'] == segment["points"]['external']['angle']:
            angle = round(segment["points"]['internal']['angle'])

            # if angle % dtick:
            if True:
                trace = dict(
                    type="scatterpolar",
                    mode='lines',
                    r=[
                        segment["points"]['internal']['radius'],
                        segment["points"]['external']['radius'],
                    ],
                    theta=[
                        angle,
                        angle,
                    ],
                    opacity=segment["opacity"],
                    visible=segment['visible'],
                    showlegend=False,
                    line=dict(
                        dash=segment["line"]['dash'],
                        color=segment["line"]['color'],
                        width=segment["line"]['width'],
                    ),
                    hoverinfo='none',
                )

                traces.append(trace)

    return traces


def get(data):
    traces = [get_pie(data['pie'])]
    traces.extend(
        get_ticks(data['segments']),
    )
    return traces
