# # coding=utf-8
# """
# Created on 2020, May 7th
# @author: orion
# """
# from transcend.views.charts.theme.models import Model as BaseModel
# from transcend.views.charts.theme.constants import WHEEL
# from transcend.views.charts.theme.zodiac.constants import get_domain
#
#
# class Model(BaseModel):
#
#     def __init__(self, chart_name):
#         super(Model, self).__init__(chart_name)
#
#     def get_zodiac_pie_center_radius(self, wheel):
#         rmax, rmin, domain = self.get_zodiac_pie_bounds(wheel)
#         return (domain['x'][1] - domain['x'][0]) * (rmax - (rmax-rmin) / 2.0)
#
#     def get_zodiac_pie_bounds(self, wheel):
#
#         chart_name = self.get_chart_name()
#
#         rmax = wheel[chart_name]['zodiac']['pie']['radius']['max']
#         rmin = wheel[chart_name]['zodiac']['pie']['radius']['min']
#
#         domain = get_domain(rmax)
#
#         return 1, rmin/rmax, domain
#
#     def get_houses_pie_min_radius(self, wheel):
#
#         chart_name = self.get_chart_name()
#
#         return wheel[chart_name]['houses']['pie']['radius']['min']
#
#     def get_houses_pie_max_radius(self, wheel):
#
#         chart_name = self.get_chart_name()
#
#         return wheel[chart_name]['houses']['pie']['radius']['max']
#
#     def get_houses_pie_bounds(self, wheel):
#
#         rmin = self.get_houses_pie_min_radius(wheel)
#         rmax = self.get_houses_pie_max_radius(wheel)
#
#         domain = get_domain(rmax)
#
#         return 1, rmin/rmax, domain
#
#     def get_houses_lines_bounds(self, wheel):
#
#         internal_radius = self.get_planets_graduations(wheel)['radius']['max']
#         external_radius = self.get_houses_pie_max_radius(wheel)
#
#         return dict(
#             radius=dict(
#                 min=internal_radius,
#                 max=external_radius,
#             )
#         )
#
#     def get_points_lines_bounds(self, wheel):
#
#         return self.get_houses_lines_bounds(wheel)
#
#     def get_planets_graduations(self, wheel):
#
#         rmax, rmin, domain = self.get_zodiac_pie_bounds(wheel)
#
#         internal_radius = rmax * (domain['x'][1] - domain['x'][0])
#         external_radius = internal_radius + WHEEL["graduations"]["circle"]["size"]
#         return dict(
#             radius=dict(
#                 min=internal_radius,
#                 max=external_radius,
#             )
#         )
#
#     def get_planets_lines(self, wheel):
#
#         external_radius = wheel["planets"][self.get_theme()]['radius']
#
#         return dict(
#             radius=dict(
#                 min=self.get_planets_graduations(wheel)['radius']['max'],
#                 max=external_radius,
#             )
#         )
#
#     def get_conjunction_radius(self):
#         planets_lines = self.get_planets_lines()
#         radius = planets_lines['radius']['max']
#         return radius
#
#     def get_aspects_circle_radius(self):
#         chart_name = self.get_chart_name()
#         return WHEEL[chart_name]['aspects']['circle']['radius']
#
#     def get_aspects_graduations(self):
#
#         rmax, rmin, domain = self.get_zodiac_pie_bounds()
#
#         external_radius = rmin * (domain['x'][1] - domain['x'][0])
#         internal_radius = self.get_aspects_circle_radius()
#
#         return dict(
#             radius=dict(
#                 min=internal_radius,
#                 max=external_radius,
#             )
#         )
