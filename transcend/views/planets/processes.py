# # coding=utf-8
# """
# Created on 2020, March 10th
# @author: orion
# """
# import numpy as np
# import copy
#
# from transcend.views.charts.wheel.images import get_coordinates
# from transcend.views.charts.wheel.images import get as get_image
#
# # from .constants import PLANETS_WHEEL_DTHETA
# # from .constants import PLANETS_WHEEL_SCALE_MIN
# # from .constants import PLANETS_WHEEL_SCALE_MAX
# from transcend.views.constants import PLANET_ICONS
# # from transcend.views.charts.transcend.constants import PIE_RADIUS_MARGIN
#
# from transcend.views.charts.wheel.planets.planets.constants import get_text_position
#
# nplanets_on_same_radius = 4
#
# # def get_customized_image(angle):
# #     sizex = PLANET_ICON_SIZE
# #     sizey = PLANET_ICON_SIZE
# #     opacity = PLANET_ICON_OPACITY
# #
# #     xanchor = "center"
# #     yanchor = "middle"
# #     rmargin = - PIE_RADIUS_MARGIN
# #
# #     textposition = get_text_position(angle)
# #
# #     return get_image_arguments(sizex, sizey, xanchor, yanchor, opacity, textposition, rmargin=rmargin)
#
#
# class Process(object):
#
#     def __init__(
#             self,
#             model,
#             chart_definition,
#     ):
#             self.model = None
#             self.chart_definition = dict()
#             self.not_planets = []
#             self.locations = dict()
#             self.asc = dict()
#             self.mc = dict()
#             self.desc = dict()
#             self.fc = dict()
#             self.init(model, chart_definition)
#
#     def init(self, model, chart_definition):
#         self.model = model
#         self.chart_definition = chart_definition
#         self.not_planets = [
#             'mean apogee',
#             'mean node',
#             'night pars',
#             'Asc',
#             'Mc',
#             'day pars',
#         ]
#         self.process()
#
#     def get_locations(self):
#         return self.locations
#
#     def process(self):
#         self.load_locations()
#         self.set_wheel_positions()
#         self.set_asc()
#         self.set_mc()
#         self.set_desc()
#         self.set_fc()
#
#     # def get_source(self, key):
#     #     if key not in PLANET_ICONS.keys():
#     #         wkey = "unknown"
#     #         wkey = "sun"
#     #     else:
#     #         wkey = key
#     #     return PLANET_ICONS[wkey]
#
#     # def is_planet(self, name):
#     #     return name not in self.not_planets
#     #
#     # def validate(self, data):
#     #     for not_planet in self.not_planets:
#     #         if not_planet in data.keys():
#     #             data.pop(not_planet)
#     #     return data
#
#     def update_label(self, image):
#         angles = sorted(self.model.get_tropical()['zodiac']['values'] % 360)
#         angle = image['angle']
#         i = 0
#         if angle < angles[0]:
#             angle += 360
#             elongation = angle - angles[-1]
#         else:
#             nangles = len(angles)
#             eod = False
#
#             while not eod and angles[i] < angle:
#                 i += 1
#                 if i == nangles - 1:
#                    eod = True
#
#             if i - 1 >= 0:
#                 elongation = angle - angles[i-1]
#             else:
#                 elongation = None
#
#         if not elongation:
#             label = "N.C.°"
#         else:
#             label = "{}°".format(
#
#                 int(
#
#                     round(elongation),
#
#                 )
#
#             )
#         image['label'] = label
#         return image
#
#     def set_wheel_positions(self):
#
#         radii = self.get_wheel_radii()
#
#         for image in self.locations:
#             image['r'] = radii[0]
#             image.update(
#                 copy.deepcopy(self.chart_definition['images']),
#             )
#             angle = image['angle_on_wheel']
#             image.update(get_coordinates(angle, image['r'], rmargin=image['rmargin']))
#
#     def load_locations(self):
#         dtheta = self.chart_definition['position']['dtheta']
#         data = copy.deepcopy(
#             self.model.get_planets(),
#         )
#         data = self.validate(data)
#         angles = []
#         planet_names = []
#         for key in data.keys():
#             angles.append(data[key]['angle'])
#             planet_names.append(key)
#
#         sorted_indices = np.argsort(angles)
#
#         angles = np.array(angles)
#         planet_names = np.array(planet_names)
#
#         angles = angles[sorted_indices]
#         planet_names = planet_names[sorted_indices]
#
#         dangle = angles[0] + 360 - angles[-1]
#         i = 1
#         while dangle < 2 * dtheta:
#             dangle = angles[i] - angles[i-1]
#             i += 1
#
#         angles = np.roll(angles, -(i-1))
#         planet_names = np.roll(planet_names, -(i-1))
#
#         processed_angles = np.array([])
#
#         locations = []
#
#         for i in range(len(angles)):
#             angle = angles[i]
#             planet_name = planet_names[i]
#             image = get_image(planet_name, angle, self.get_source(planet_name))
#             image['planet'] = planet_name
#             image['angle'] = angle
#             image.update(
#                 get_text_position(angle),
#             )
#             image = self.update_label(image)
#
#             # new angle calculation if no enough place to display de image in front of angle graduation
#
#             angle_on_wheel = angle
#             if len(processed_angles) > 0:
#                 dangle = angle - processed_angles[-1]
#                 if dangle < dtheta:
#                     angle_on_wheel = processed_angles[-1] + dtheta
#
#             image['angle_on_wheel'] = angle_on_wheel
#             locations.append(image)
#             processed_angles = np.append(processed_angles, [angle_on_wheel])
#
#         self.locations = locations
#
#     def get_location(self, name):
#         res = dict()
#         found = False
#         for location in self.locations:
#             if location['planet'] == name:
#                 found = True
#             if found:
#                 break
#
#         if found:
#             res = {'angle': location['angle'], 'r': location['r']}
#         else:
#             print('t')
#         return res
#
#     # def get_wheel_nrows(self):
#     #     nrows = 0
#     #     for key in self.locations.keys():
#     #         cols = self.locations[key]
#     #         if len(cols) > nrows:
#     #             nrows = len(cols)
#     #     return nrows
#
#     def get_wheel_radii(self):
#
#         nrows = 1  # self.get_wheel_nrows()
#
#         # atomic size for a planet display
#
#         sizex = self.chart_definition['images']['sizex']
#         text_size = sizex
#
#         dr = 0.025
#
#         widget_size = sizex + text_size + 2 * dr
#
#         # rmin = self.chart_definition['position']['radius']['min']
#         rmax = self.chart_definition['position']['radius']['max_4']
#         rmargin = self.chart_definition['position']['radius']['margin'] / nrows
#
#         planet_rmax = rmax - rmargin
#
#         wradii = planet_rmax - 0.5 * widget_size - widget_size * np.array(list(range(nrows)))
#
#         radii = list(wradii)
#
#         return radii
#
#     def get_planet(self, key, label=None):
#         res = copy.deepcopy(
#             self.model.get_planets()[key],
#         )
#         if not label:
#             label = key
#         res.update({'label': label})
#         return res
#
#     def set_asc(self):
#         key = 'Asc'
#         self.asc = self.get_planet(key, 'AS')
#
#     def set_desc(self):
#         key = 'Asc'
#         self.desc = copy.deepcopy(
#             self.get_planet(key)
#         )
#         self.desc['angle'] += 180
#         self.desc['angle'] = self.desc['angle'] % 360
#         self.desc['label'] = 'DE'
#
#     def get_asc(self):
#         return self.asc
#
#     def get_desc(self):
#         return self.desc
#
#     def set_mc(self):
#         key = 'Mc'
#         self.mc = self.get_planet(key, "MC")
#
#     def set_fc(self):
#         key = 'Mc'
#         self.fc = copy.deepcopy(
#             self.get_planet(key)
#         )
#         self.fc['angle'] += 180
#         self.fc['angle'] = self.fc['angle'] % 360
#         self.fc['label'] = 'FC'
#
#     def get_mc(self):
#         return self.mc
#
#     def get_fc(self):
#         return self.fc
#
#     def get_data(self):
#         return {
#             'rmin': self.chart_definition['position']['radius']['min'],
#             'locations': self.get_locations(),
#             'asc': self.get_asc(),
#             'desc': self.get_desc(),
#             'mc': self.get_mc(),
#             'fc': self.get_fc(),
#         }
