# coding=utf-8
"""
Created on 2020, May 7th
"""
from transcend.views.charts.theme.models import Model as BaseModel

from transcend.views.charts.graphics.constants import DIMENSIONS
from transcend.views.charts.theme.zodiac.constants import get_domain


class Model(BaseModel):

    def __init__(self, chart_name, sub_chart_name):
        super(Model, self).__init__(chart_name)
        self.sub_chart_name = sub_chart_name

    def get_zodiac_pie_center_radius_tropical(self):
        rmax, rmin, domain = self.get_zodiac_pie_bounds_tropical()
        return (domain['x'][1] - domain['x'][0]) * (rmax - (rmax-rmin) / 2.0)

    def get_zodiac_pie_bounds(self, zodiactype="tropical"):

        chart_name = self.get_chart_name()

        rmax = DIMENSIONS[chart_name][zodiactype]['zodiac']['pie']['radius']['max']
        rmin = DIMENSIONS[chart_name][zodiactype]['zodiac']['pie']['radius']['min']

        domain = get_domain(rmax)

        return 1, rmin/rmax, domain

    def get_zodiac_pie_bounds_tropical(self):
        return self.get_zodiac_pie_bounds()

    def get_zodiac_pie_bounds_sidereal(self):
        return self.get_zodiac_pie_bounds(zodiactype="sidereal")

    def get_houses_pie_min_radius(self, zodiactype="tropical"):

        chart_name = self.get_chart_name()

        return DIMENSIONS[chart_name][zodiactype]['houses']['pie']['radius']['min']

    def get_houses_pie_max_radius(self, zodiactype="tropical"):

        chart_name = self.get_chart_name()

        return DIMENSIONS[chart_name][zodiactype]['houses']['pie']['radius']['max']

    def get_houses_pie_bounds_tropical(self):

        rmin = self.get_houses_pie_min_radius()
        rmax = self.get_houses_pie_max_radius()

        domain = get_domain(rmax)

        return 1, rmin/rmax, domain

    def get_houses_pie_bounds(self, zodiactype="tropical"):

        rmin = self.get_houses_pie_min_radius(zodiactype=zodiactype)
        rmax = self.get_houses_pie_max_radius(zodiactype=zodiactype)

        domain = get_domain(rmax)

        return 1, rmin/rmax, domain

    def get_houses_lines_bounds_tropical(self):

        rmin = self.get_planets_graduations()['radius']['max']
        rmax = self.get_houses_pie_max_radius()

        return dict(
            radius=dict(
                min=rmin,
                max=rmax,
            )
        )

    def get_houses_lines_bounds(self, zodiactype="tropical"):

        rmin = self.get_planets_graduations()['radius']['max']
        rmax = self.get_houses_pie_max_radius(zodiactype=zodiactype)

        return dict(
            radius=dict(
                min=rmin,
                max=rmax,
            )
        )

    def get_houses_lines_bounds_sidereal(self):

        rmin = self.get_planets_graduations()['radius']['max']
        rmax = self.get_houses_pie_max_radius(zodiactype="sidereal")

        return dict(
            radius=dict(
                min=rmin,
                max=rmax,
            )
        )

    def get_points_lines_bounds(self, zodiactype="tropical"):

        return self.get_houses_lines_bounds(zodiactype=zodiactype)

    def get_planets_graduations(self):

        rmax, rmin, domain = self.get_zodiac_pie_bounds_tropical()

        rmin = rmax * (domain['x'][1] - domain['x'][0])
        rmax = rmin + DIMENSIONS["graduations"]["circle"]["size"]
        return dict(
            radius=dict(
                min=rmin,
                max=rmax,
            )
        )

    def get_planets_lines(self):

        return dict(
            radius=dict(
                min=self.get_planets_graduations()['radius']['max'],
                max=DIMENSIONS["planets"][self.get_theme()]['radius'],
            )
        )

    def get_conjunction_radius(self):
        planets_lines = self.get_planets_lines()
        radius = planets_lines['radius']['max']
        return radius

    def get_aspects_circle_radius(self, zodiactype="tropical"):
        chart_name = self.get_chart_name()
        return DIMENSIONS[chart_name][zodiactype]['aspects']['circle']['radius']

    def get_aspects_graduations(self, zodiactype="tropical"):

        rmax, rmin, domain = self.get_zodiac_pie_bounds_sidereal()

        external_radius = rmin * (domain['x'][1] - domain['x'][0])
        internal_radius = self.get_aspects_circle_radius(zodiactype=zodiactype)

        return dict(
            radius=dict(
                min=internal_radius,
                max=external_radius,
            )
        )







    # def get_zodiac_pie(self, sub_chart_name=""):
    #     chart_name = self.get_chart_name()
    #     if not sub_chart_name:
    #         sub_chart_name = self.get_sub_chart_name()
    #     if sub_chart_name:
    #         rmax = DIMENSIONS[chart_name][sub_chart_name]['zodiac']['pie']['radius']['max']
    #         rmin = DIMENSIONS[chart_name][sub_chart_name]['zodiac']['pie']['radius']['min']
    #
    #     else:
    #         rmax = DIMENSIONS[chart_name]['zodiac']['pie']['radius']['max']
    #         rmin = DIMENSIONS[chart_name]['zodiac']['pie']['radius']['min']
    #
    #     domain = get_domain(rmax)
    #
    #     return 1, rmin/rmax, domain
    #
    # def get_houses_pie(self, sub_chart_name=""):
    #     chart_name = self.get_chart_name()
    #     if not sub_chart_name:
    #         sub_chart_name = self.get_sub_chart_name()
    #     if sub_chart_name:
    #         rmin = DIMENSIONS[chart_name][sub_chart_name]['houses']['pie']['radius']['min']
    #         rmax = DIMENSIONS[chart_name][sub_chart_name]['houses']['pie']['radius']['max']
    #
    #     else:
    #         rmin = DIMENSIONS[chart_name]['houses']['pie']['radius']['min']
    #         rmax = DIMENSIONS[chart_name]['houses']['pie']['radius']['max']
    #
    #     # rmin = self.get_graduations()['radius']['external']
    #
    #     domain = get_domain(rmax)
    #
    #     return 1, rmin/rmax, domain
    #
    # def get_zodiac_pie_center_radius(self):
    #     rmax, rmin, domain = self.get_zodiac_pie()
    #     return (domain['x'][1] - domain['x'][0]) * (rmax - (rmax-rmin) / 2.0)
    #
    # def get_planets_graduations(self):
    #
    #     rmax, rmin, domain = self.get_zodiac_pie()
    #
    #     internal_radius = rmax * (domain['x'][1] - domain['x'][0])
    #     external_radius = internal_radius + DIMENSIONS["graduations"]["circle"]["size"]
    #     return dict(
    #         radius=dict(
    #             internal=internal_radius,
    #             external=external_radius,
    #         )
    #     )
    #
    # def get_aspects_graduations(self, sub_chart_name=""):
    #
    #     rmax, rmin, domain = self.get_zodiac_pie(sub_chart_name=sub_chart_name)
    #
    #     external_radius = rmin * (domain['x'][1] - domain['x'][0])
    #     internal_radius = self.get_aspects_circle_radius(sub_chart_name=sub_chart_name)
    #
    #     return dict(
    #         radius=dict(
    #             internal=internal_radius,
    #             external=external_radius,
    #         )
    #     )
    #
    # def get_planets_lines(self):
    #
    #     external_radius = DIMENSIONS["planets"][self.get_theme()]['radius']
    #
    #     return dict(
    #         radius=dict(
    #             internal=self.get_planets_graduations()['radius']['external'],
    #             external=external_radius,
    #         )
    #     )
    #
    # def get_aspects_circle_radius(self, sub_chart_name=""):
    #     # if self.get_sub_chart_name():
    #     #     rmax, rmin, domain = self.get_zodiac_pie(sub_chart_name="sidereal")
    #     # else:
    #     #     rmax, rmin, domain = self.get_zodiac_pie()
    #     #
    #     # return rmin * (domain['x'][1] - domain['x'][0])
    #     chart_name = self.get_chart_name()
    #     if not sub_chart_name:
    #         sub_chart_name = self.get_sub_chart_name()
    #     if sub_chart_name:
    #         radius = DIMENSIONS[chart_name][sub_chart_name]['aspects']['circle']['radius']
    #     else:
    #         radius = DIMENSIONS[chart_name]['aspects']['circle']['radius']
    #     return radius
    #
    # def get_houses_external_pie_radius(self, sub_chart_name=""):
    #     chart_name = self.get_chart_name()
    #     if not sub_chart_name:
    #         sub_chart_name = self.get_sub_chart_name()
    #     if sub_chart_name:
    #         rmax = DIMENSIONS[chart_name][sub_chart_name]['houses']['pie']['radius']['max']
    #
    #     else:
    #         rmax = DIMENSIONS[chart_name]['houses']['pie']['radius']['max']
    #
    #     return rmax
    #
    # def get_houses_bounds(self):
    #
    #     internal_radius = self.get_planets_graduations()['radius']['external']
    #     external_radius = self.get_houses_external_pie_radius()
    #
    #     return dict(
    #         radius=dict(
    #             min=internal_radius,
    #             max=external_radius,
    #         )
    #     )
    #
    # def get_points_bounds(self):
    #
    #     return self.get_houses_bounds()
