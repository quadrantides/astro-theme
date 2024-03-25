# coding=utf-8
"""
Created on 2020, April 24th
@author: orion
"""
import math
import numpy as np


# def get_display_order(box_size, angles):
#
#     orders = list(range(len(angles)))
#
#     sorted_indices = np.argsort(angles)
#
#     orders = np.array(orders)
#     angles = np.array(angles)
#
#     angles = angles[sorted_indices]
#     orders = orders[sorted_indices]
#
#     dangle = angles[0] + 360 - angles[-1]
#     i = 1
#     while dangle < 2 * box_size:
#         dangle = angles[i] - angles[i - 1]
#         i += 1
#
#     orders = np.roll(orders, -(i - 1))
#
#     return orders.tolist()


def get_circle_coordinates(point):

    point_radius = point['radius']
    point_angle = point['angle']

    diameter = 0.05
    nb_points = 26
    center_radius = diameter / 2.0

    circle_theta = 2 * math.pi * np.array(range(nb_points)) / (nb_points - 1)

    x_circle = np.array([center_radius * math.cos(circle_theta[i]) for i in range(nb_points)])
    y_circle = np.array([center_radius * math.sin(circle_theta[i]) for i in range(nb_points)])

    x = x_circle + (point_radius - center_radius) * math.cos((point_angle * math.pi) / 180)
    y = y_circle + (point_radius - center_radius) * math.sin((point_angle * math.pi) / 180)

    x = x.tolist()
    y = y.tolist()

    theta = np.array([math.atan2(y[i], x[i]) for i in range(nb_points)])
    angles = theta * 180 / math.pi
    angles = angles.tolist()

    radii = [x[i] / math.cos(theta[i]) for i in range(nb_points)]

    return dict(
        radius=radii,
        angle=angles,
    )


def get_segment_coordinates(point1, point2):

    r1 = point1['radius']
    theta1 = point1['angle']
    r2 = point2['radius']
    theta2 = point2['angle']

    p1x = r1*math.cos((theta1 * math.pi) / 180)
    p1y = r1*math.sin((theta1 * math.pi) / 180)

    p2x = r2*math.cos((theta2 * math.pi) / 180)
    p2y = r2*math.sin((theta2 * math.pi) / 180)

    nb_points = 100

    if abs(p2x - p1x) < 1e-3:

        x = [p1x] * nb_points
        dy = p2y - p1y
        y = p1y + dy * np.array(range(nb_points)) / (nb_points - 1)
        y = y.tolist()
    else:
        a = (p2y - p1y) / (p2x - p1x)
        b = p1y - a * p1x

        dx = p2x - p1x
        x = p1x + dx * np.array(range(nb_points)) / (nb_points - 1)
        y = a * x + b
        x = x.tolist()
        y = y.tolist()

    theta = np.array([math.atan2(y[i], x[i]) for i in range(nb_points)])
    angles = theta * 180 / math.pi
    angles = angles.tolist()

    radii = [x[i] / math.cos(theta[i]) for i in range(nb_points)]

    return dict(
        radius=radii,
        angle=angles,
    )
