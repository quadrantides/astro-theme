# # coding=utf-8
# """
# Created on 2020, Jan 13th
# @author: orion
# """
#
#
# def get_pie_args(angles):
#
#     bound_min_angles = angles
#     bound_max_angles = angles[1::]
#     bound_max_angles.append(angles[0])
#
#     res = {
#         'rotation': 90 - angles[1],
#         'values': [],
#     }
#
#     for i, bound_min_angle in enumerate(bound_min_angles):
#         bound_max_angle = bound_max_angles[i]
#         if bound_max_angle <= bound_min_angle:
#             bound_max_angle += 360
#
#         size = bound_max_angle - bound_min_angle
#         res['values'].append(size)
#
#     return res
