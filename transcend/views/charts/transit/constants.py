# # coding=utf-8
# """
# Created on 2020, August 15th
# @author: orion
#
# Calculation are given in cartesian coordinates
#
# """
# from transcend.views.charts.theme.houses.constants import COLORS as HOUSES_COLORS
#
# VERSION = "1.0"
#
# GRADUATIONS_TICKLEN = 0
#
# LAYOUT_WIDTH_PX = LAYOUT_WIDTH_PY = 680  # 720  # 1140 960 720 540
# # XAXIS_RANGE = YAXIS_RANGE = [-1.25, 1.25]
# XAXIS_RANGE = YAXIS_RANGE = [-1, 1]
# PIE_RADIUS_MARGIN = 10
# # POLAR_DOMAIN_X = POLAR_DOMAIN_Y = [0.1, 0.9]
# POLAR_DOMAIN_X = POLAR_DOMAIN_Y = [0.15, 0.85]
# POLAR_DOMAIN_X = POLAR_DOMAIN_Y = [0.2, 0.8]
# POLAR_DOMAIN_X = POLAR_DOMAIN_Y = [0.0, 1.0]
#
# SCALE_FACTOR = 1 / (POLAR_DOMAIN_X[1] - POLAR_DOMAIN_X[0])
#
# WHEEL_WIDTH_PX = LAYOUT_WIDTH_PX
# WHEEL_HEIGHT_PX = WHEEL_WIDTH_PX
#
# POLAR_PLOT_RADIUS_PX = LAYOUT_WIDTH_PX * (POLAR_DOMAIN_X[1] - POLAR_DOMAIN_X[0])
#
# charts = ['planets', "graduations", "zodiac"]
#
# radii = \
#     dict(
#         max=[0.6, 0.425, 0.275],
#         min=[0.6, 0.275, 0.275],
#     )
#
# radii = \
#     dict(
#         max=[0.95, 0.825, 0.625],
#         min=[0.95, 0.775, 0.625],
#     )
#
# radii = \
#     dict(
#         max=[0.85, 0.775, 0.625],
#         min=[0.85, 0.775, 0.625],
#     )
#
# ASPECTS_GRADUATIONS_SIZE = 0 # 0.025
# THEME_ASPECTS_RADIUS = radii['min'][1] # - ASPECTS_GRADUATIONS_SIZE
#
# PLANETS_RADIUS = radii['max'][0]
#
# GRADUATIONS_CIRCLE_SIZE = 0.04
#
# ZODIAC_PIE_RMAX_PX = radii['max'][1]
# ZODIAC_PIE_RMIN_PX = radii['min'][1]
#
# COMPOUNDED_SIDEREAL_ZODIAC_PIE_RMAX = radii['max'][2]
# COMPOUNDED_SIDEREAL_ZODIAC_PIE_RMIN = radii['min'][2]
#
# # DONUT_SIZE_PX = 60
#
# # RMAX_PX = (WHEEL_WIDTH_PX - GRADUATIONS_CIRCLE_SIZE_PX) * (POLAR_DOMAIN_X[1] - POLAR_DOMAIN_X[0])
#
#
# # ZODIAC_RMAX_PX = RMAX_PX
# # ZODIAC_DONUT_SIZE_PX = RMAX_PX * fractions[0]
# # ZODIAC_RMIN_PX = ZODIAC_RMAX_PX - ZODIAC_DONUT_SIZE_PX
#
# # HOUSES
#
# HOUSES_RMAX = 1.075
# HOUSES_DR = 0.15
#
# # HOUSES_RMIN_PX = PLANETS_PIE_RMAX_PX
# #
#
#
# # RMIN_PX = RMAX_PX - DONUT_SIZE_PX
#
# # SIDEREAL_RMIN_PX = RMIN_PX - DONUT_SIZE_PX
#
# # EXTERNAL_HOUSES_LINES_RADIUS_PX = WHEEL_WIDTH_PX - GRADUATIONS_CIRCLE_SIZE_PX - DONUT_SIZE_PX
#
#
# # EXTERNAL_DONUT_SIZE_PX = 20
# # EXTERNAL_HOUSES_RADIUS_PX = RMIN_PX - EXTERNAL_DONUT_SIZE_PX
#
#
# # GRADUATIONS_CIRCLE_RADIUS_PX = POLAR_DOMAIN_X[1] * LAYOUT_WIDTH_PX + 25
#
# # GRADUATIONS_RADIUS_PX = 1 - 1.0 * GRADUATIONS_TICKLEN / WHEEL_WIDTH_PX
#
#
# # SIDEREAL_DONUT_SIZE_PX = DONUT_SIZE_PX
# # TROPICAL_DONUT_SIZE_PX = 50
#
#
# # SIDEREAL_RMIN_PX_FOR_EXPANSED_CHART = RMIN_PX - SIDEREAL_DONUT_SIZE_PX
# # TROPICAL_RMAX_PX = SIDEREAL_RMIN_PX_FOR_EXPANSED_CHART + TROPICAL_DONUT_SIZE_PX
#
# # SIDEREAL_RMIN_PX_FOR_COLLAPSED_CHART = TROPICAL_RMAX_PX
# # TROPICAL_RMIN_PX = TROPICAL_RMAX_PX - TROPICAL_DONUT_SIZE_PX
#
# # THEME_ASPECTS_RADIUS = 300  # 250
# TRANSIT_ASPECTS_RADIUS = 120
#
# PLANETS_BOX_SIZE = 10
# NB_PLANETS_BOXES = int(360 / PLANETS_BOX_SIZE)
#
# # GRADUATIONS_RADIUS_MIN_PX = TROPICAL_RMIN_PX - 30
# WHEEL = {
#     'layout': dict(
#         width=LAYOUT_WIDTH_PX,
#         height=LAYOUT_WIDTH_PY,
#         polar=dict(
#             domain=dict(
#                 x=POLAR_DOMAIN_X,
#                 y=POLAR_DOMAIN_Y,
#             ),
#             angularaxis=dict(
#                 ticklen=GRADUATIONS_TICKLEN,
#                 dtick=1,
#             ),
#         ),
#         xaxis=dict(
#             range=XAXIS_RANGE,
#         ),
#         yaxis=dict(
#             range=YAXIS_RANGE,
#         ),
#     ),
#     'width': WHEEL_WIDTH_PX,
#     'height': WHEEL_HEIGHT_PX,
#
#     'color': {
#         'tropical':  "#ff0066",
#     },
#     'title': {
#         'position': {
#             'top': {
#                 'left': {
#                     'sorted_items': [
#                         "transit identifier",
#                         "theme identifier",
#                         "date",
#                         'location',
#                         'latlon title',
#                         'latlon value',
#                         'houses_system',
#                         'mode',
#                     ],
#                     "x0": -0.12,
#                     "y0": 0.975,
#                     "step": 0.03,
#                 },
#                 'right': {
#                     "x0": 0.95,
#                     "y0": 0.95,
#                     "step": 0.03,
#                 },
#             },
#             'bottom': {
#                 'left': {
#                     'sorted_items': [
#                         'tropical title',
#                         'tropical houses_system',
#                     ],
#                     "x0": -0.12,
#                     "y0": 0.2,
#                     "step": 0.03,
#                 },
#
#                 'right': {
#                     'sorted_items': [
#                         'sidereal title',
#                         'sidereal houses_system',
#                         'sidereal mode',
#                     ],
#                     "x0": 0.975,
#                     "y0": 0.2,
#                     "step": 0.03,
#                 },
#             }
#
#         },
#
#     },
#     'graduations': dict(
#         theme=dict(
#             circle=dict(
#                 size=0.04,
#             ),
#             rmin=0.425,
#         ),
#         transit=dict(
#             circle=dict(
#                 size=GRADUATIONS_CIRCLE_SIZE,
#             ),
#             rmin=ZODIAC_PIE_RMAX_PX,
#         ),
#     ),
#     'houses': dict(
#         annotations=dict(
#             radius=dict(
#                 internal=HOUSES_RMAX - HOUSES_DR,
#                 external=HOUSES_RMAX,
#             ),
#         ),
#         lines=dict(
#             radius=dict(
#                 external=HOUSES_RMAX,
#             ),
#         ),
#         # theme=dict(
#         #     annotations=dict(
#         #         radius=dict(
#         #             internal=1 - 0.15,
#         #             external=1 - 0.6 * 0.15,
#         #         ),
#         #     ),
#         #     lines=dict(
#         #         radius=dict(
#         #             external=1,
#         #         ),
#         #     ),
#         # ),
#         # transit=dict(
#         #     annotations=dict(
#         #         radius=dict(
#         #             internal=1.075 - 0.15,
#         #             external=1.075 - 0.6 * 0.15,
#         #         ),
#         #     ),
#         #     lines=dict(
#         #         radius=dict(
#         #             external=1.075,
#         #         ),
#         #     ),
#         # ),
#     ),
#     'planets': {
#         'theme': {
#             'radius': 0.6,
#         },
#         'transit': {
#             'radius': PLANETS_RADIUS,
#         },
#
#         'box_size': PLANETS_BOX_SIZE,  # in degrees
#         'line': {
#             'color': '#000',
#         },
#         'image': {
#             'size': 0.075,
#         },
#     },
#     'points': {
#         'line': {
#             'color': '#fac673',
#         },
#     },
#     'aspects': {
#         'transit': {
#             'circle': {
#                 'radius': THEME_ASPECTS_RADIUS,
#             },
#         },
#     },
#     'sidereal': {
#         'zodiac': {
#             'pie': {
#                 'radius': {
#                     'min': ZODIAC_PIE_RMIN_PX,
#                     'max': ZODIAC_PIE_RMAX_PX,
#                 },
#                 'colors': ["#fff"] * 12,
#             },
#         },
#         "houses": dict(
#             pie=dict(
#                 radius=dict(
#                     min=HOUSES_RMAX - HOUSES_DR,
#                     max=HOUSES_RMAX - 0.6 * HOUSES_DR,
#                 ),
#                 colors=HOUSES_COLORS,
#             ),
#         ),
#         'aspects': {
#             'circle': {
#                 'radius': THEME_ASPECTS_RADIUS,
#             },
#         },
#     },
#     'tropical': {
#         'zodiac': {
#             'pie': {
#                 'radius': {
#                     'min': ZODIAC_PIE_RMIN_PX,
#                     'max': ZODIAC_PIE_RMAX_PX,
#                 },
#                 'colors': ["#fff"] * 12,
#             },
#         },
#         "houses": dict(
#             theme=dict(
#                 radius=dict(
#                     min=0.825 - 0.15,
#                     max=0.825 - 0.6 * 0.15,
#                 ),
#                 colors=HOUSES_COLORS,
#             ),
#             transit=dict(
#                 radius=dict(
#                     min=1.075 - 0.15,
#                     max=1.075 - 0.6 * 0.15,
#                 ),
#                 colors=HOUSES_COLORS,
#             ),
#         ),
#         'aspects': {
#             'circle': {
#                 'radius': THEME_ASPECTS_RADIUS,
#             },
#         },
#     },
#     'compounded': {
#         'tropical': {
#             'zodiac': {
#                 'pie': {
#                     'radius': {
#                         'min': ZODIAC_PIE_RMIN_PX,
#                         'max': ZODIAC_PIE_RMAX_PX,
#                     },
#                     'colors': ["#fff"] * 12
#                 },
#             },
#             "houses": dict(
#                 pie=dict(
#                     radius=dict(
#                         min=HOUSES_RMAX - HOUSES_DR,
#                         max=HOUSES_RMAX - 0.6 * HOUSES_DR,
#                     ),
#                     colors=HOUSES_COLORS,
#                 ),
#             ),
#             'aspects': {
#                 'circle': {
#                     'radius': THEME_ASPECTS_RADIUS,
#                 },
#             },
#         },
#         'sidereal': {
#             'zodiac': {
#                 'pie': {
#                     'radius': {
#                         'min': COMPOUNDED_SIDEREAL_ZODIAC_PIE_RMIN,
#                         'max': COMPOUNDED_SIDEREAL_ZODIAC_PIE_RMAX,
#                     },
#                     'colors': ["#dedede"] * 12
#                 },
#             },
#             "houses": dict(
#                 pie=dict(
#                     radius=dict(
#                         min=HOUSES_RMAX - 0.6 * HOUSES_DR,
#                         max=HOUSES_RMAX - 0.2 * HOUSES_DR,
#                     ),
#                     colors=HOUSES_COLORS,
#                 ),
#             ),
#             'aspects': {
#                 'circle': {
#                     'radius': COMPOUNDED_SIDEREAL_ZODIAC_PIE_RMIN - ASPECTS_GRADUATIONS_SIZE,
#                 },
#             },
#         },
#
#     },
# }
#
#
# def get_polar_width():
#     scale = WHEEL['layout']["polar"]["domain"]["x"][1]
#     return scale * WHEEL['layout']["width"]
#
#
# def get_polar_width2():
#     scale = WHEEL['layout']["polar"]["domain"]["x"][1] - WHEEL['layout']["polar"]["domain"]["x"][0]
#     return scale * WHEEL['layout']["width"]
