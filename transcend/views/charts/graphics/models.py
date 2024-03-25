# coding=utf-8
"""
Created on 2020, August 25th
@author: orion
"""
from transcend.views.charts.graphics.constants import DIMENSIONS
from transcend.views.charts.graphics.zodiac.constants import get_domain


class Model(object):

    def __init__(self, dimensions=None):
        self.dimensions = DIMENSIONS if not dimensions else dimensions

    def get_polar_angularaxis_dticks(self):
        return self.dimensions["layout"]['polar']['angularaxis']['dtick']

    def get_zodiac_annotation_radius(self):
        rmax, rmin, domain = self.get_zodiac()
        return (domain['x'][1] - domain['x'][0]) * (rmax - (rmax-rmin) / 2.0)

    def get_zodiac(self):

        rmin = self.dimensions['zodiac']['radius']['internal']
        rmax = self.dimensions['zodiac']['radius']['external']

        domain = get_domain(rmax)

        return 1, rmin/rmax, domain

    def get_graduations(self):

        return dict(
            radius=dict(
                min=self.dimensions['graduations']['radius']['internal'],
                max=self.dimensions['graduations']['radius']['external'],
            )
        )

    def get_houses_lines(self):

        return dict(
            radius=dict(
                min=self.dimensions['houses']['lines']['radius']['internal'],
                max=self.dimensions['houses']['lines']['radius']['external'],
            )
        )

    def get_houses_annotations(self):
        return self.dimensions['houses']['annotations']

    def get_points_lines(self):

        return self.get_houses_lines()

    def get_planets_lines(self):
        return dict(
            radius=dict(
                min=self.dimensions["graduations"]['radius']['external'],
                max=self.dimensions["planets"]['radius'],
            )
        )

    def get_planets(self):
        return self.dimensions["planets"]

    def get_conjunction_radius(self):
        planets_lines = self.get_planets_lines()
        radius = planets_lines['radius']['max']
        return radius

    def get_aspects_radius(self):
        return self.dimensions['aspects']['radius']
