# coding=utf-8
"""
Created on 2020, March 11th
@author: orion
"""
import math


def get_coordinates(angle, r):

    # x = r0[0] + r0[0] * r * math.cos((angle * math.pi) / 180)
    # y = r0[1] + r0[1] * r * math.sin((angle * math.pi) / 180)
    x = r * math.cos((angle * math.pi) / 180)
    y = r * math.sin((angle * math.pi) / 180)

    return {
        "x": x,
        "y": y,
    }


def get_centers(angles):
    bound_min_angles = angles
    bound_max_angles = angles[1::]
    bound_max_angles.append(angles[0])

    centers = []

    for i, bound_min_angle in enumerate(bound_min_angles):
        bound_max_angle = bound_max_angles[i]
        if bound_max_angle <= bound_min_angle:
            bound_max_angle += 360

        size = bound_max_angle - bound_min_angle
        angle = bound_min_angle + (size / 2)

        centers.append(angle)

    return centers
