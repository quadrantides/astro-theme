# # coding=utf-8
# """
# Created on 2020, April 14th
# @author: orion
# """
# from transcend.processes import merge
# from transcend.models.planets.structures import get_planet_structure as get_model_planet_structure
# from transcend.views.charts.constants import get_theme_struct
#
# VERSION = "1.0"
#
#
# def get_planet_structure(chart_name, zodiactype):
#
#     structure = get_theme_struct(chart_name)
#     structure["chart"][chart_name] = {
#         zodiactype: {
#             'planet': dict(),
#         },
#     }
#
#     structure['chart'][chart_name][zodiactype] = merge(
#         get_model_planet_structure(),
#         structure['chart'][chart_name][zodiactype],
#     )
#
#     structure['chart'][chart_name][zodiactype]['planet'].update(
#         {
#             'visible': "",
#             "angle_on_chart": 0.0,
#             "label": "",
#             "image": dict(),
#             "text": {
#                 'radius': 0.0,
#                 "value": '',
#                 "position": "",
#             },
#             "line": {
#                 'color': "",
#             },
#             'graduations': {
#                 'circle': {
#                     "radius": 0.0,
#                 },
#             },
#         },
#     )
#
#     return structure
#
#
# def get_structure(chart_name, zodiactype):
#
#     structure = get_theme_struct(chart_name)
#     structure["chart"][chart_name] = {
#         zodiactype: {
#             'planets': [],
#         },
#     }
#
#     return structure
#
#
# def get_text_position(angle):
#     if angle <= 15 or angle > 315:
#         yanchor = "top"
#         xanchor = "right"
#     elif 15 < angle <= 135:
#         xanchor = "right"
#         yanchor = "bottom"
#     elif 135 < angle <= 225:
#         yanchor = "bottom"
#         xanchor = "right"
#     elif 225 < angle <= 315:
#         yanchor = "bottom"
#         xanchor = "right"
#
#     return '{} {}'.format(yanchor, xanchor)
