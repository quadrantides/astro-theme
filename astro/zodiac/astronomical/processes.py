# coding=utf-8
"""
Created on 2020, December 20th
@author: orion
"""
from astropy.coordinates import SkyCoord

from astro.zodiac.astronomical.constants import VERNAL_POINT_POSITION
from astro.zodiac.astronomical.constants import get_positions
from astro.zodiac.astronomical.constants import get_constellations_names


class Process(object):

    def __init__(self):
        self.data = dict()
        self.process()

    def get_aries_begin_longitude(self):

        # longitude begin = distance angulaire au point vernal

        de1 = VERNAL_POINT_POSITION["equatorial"]["declination"]
        ra1 = VERNAL_POINT_POSITION["equatorial"]["right_ascension"]

        name = "pisces"
        de2 = self.data[name]["end"]["equatorial"]["declination"]
        ra2 = self.data[name]["end"]["equatorial"]["right_ascension"]

        coord1 = SkyCoord(ra1, de1, unit="deg")
        coord2 = SkyCoord(ra2, de2, unit="deg")
        separation = coord1.separation(coord2)
        return separation.value

    def get_constellation_angular_distance(self, name):

        # longitude end = longitude begin + distance angulaire de la constellation

        de1 = self.data[name]["begin"]["equatorial"]["declination"]
        ra1 = self.data[name]["begin"]["equatorial"]["right_ascension"]

        coord1 = SkyCoord(ra1, de1, unit="deg")
        de2 = self.data[name]["end"]["equatorial"]["declination"]
        ra2 = self.data[name]["end"]["equatorial"]["right_ascension"]
        coord2 = SkyCoord(ra2, de2, unit="deg")
        angle = coord1.separation(coord2)
        return angle.value

    def process(self):

        self.data = get_positions()

        current_begin_longitude = self.get_aries_begin_longitude()

        for name in get_constellations_names():

            self.data[name]["begin"]["longitude"] = current_begin_longitude

            self.data[name]["end"]["longitude"] = \
                (current_begin_longitude + self.get_constellation_angular_distance(name)) % 360

            current_begin_longitude = self.data[name]["end"]["longitude"]

    def get_data(self):
        return self.data
