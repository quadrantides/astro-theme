# coding=utf-8
"""
Created on 2020, April 22th
@author=orion
"""
import numpy as np
VERSION = "1.0"


def get_points(radius):

    npoints = 500
    r = radius + np.zeros(npoints)
    theta = 360 * np.array(range(npoints)) / (npoints - 1)
    return r.tolist(), theta.tolist()


def get_circle(data, r, theta):

    return \
        dict(
            type="scatterpolar",
            mode='lines',
            r=r,
            theta=theta,
            opacity=data["opacity"],
            visible=data['visible'],
            name=data['name'],
            showlegend=False,
            line=dict(
                width=data['line']['width'],
                color=data['line']['color'],
            ),
            hoverinfo='none',
        )


def get_ticks(data):

    traces = []

    for i in range(0, 360, data["ticks"]["dtick"]):
        dr = data["radius"]['max'] - data["radius"]['min']
        mod10 = i % 10
        mod5 = i % 5
        tens = mod10 == 0
        if tens:
            color = data["ticks"]["tick"]["tens"]['color']
            width = data["ticks"]["tick"]["tens"]['width']
            ticklen = 0.0
        elif mod5 == 0:
            ticklen = 0.3
            color = data["ticks"]["tick"]["tens"]['color']
            width = data["ticks"]["tick"]["tens"]['width']
        else:
            color = data["ticks"]["tick"]["others"]['color']
            width = data["ticks"]["tick"]["others"]['width']
            ticklen = 0.65

        tick = dict(
            type="scatterpolar",
            mode='lines',
            r=[data["radius"]['min'] + ticklen * dr, data["radius"]['max']],
            theta=[i, i],
            opacity=data["opacity"],
            visible=data['visible'],
            showlegend=False,
            line=dict(
                color=color,
                width=width,
            ),
            hoverinfo='none',
        )

        traces.append(tick)

    return traces


def get(data):

    rmin, thetamin = get_points(data['radius']['min'])
    rmax, thetamax = get_points(data['radius']['max'])

    traces = [
        get_circle(data, rmin, thetamin),
        get_circle(data, rmax, thetamax),
    ]

    traces.extend(
        get_ticks(data),
    )
    return traces
