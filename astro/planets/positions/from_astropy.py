# coding=utf-8
"""
Created on 2020, June 11th
@author: orion
"""
import numpy as np
from astropy.time import Time
from astropy.coordinates import SkyCoord
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body_barycentric, get_body, get_moon


DATE_FORMAT = "%Y-%m-%d %H:%M"

COLORS = {1: 'red', 6: 'blue', 8: 'green'}


def create_dates_generator(dates):

    for date in dates:
        yield Time(date)


def create_right_ascension_generator(dates, planet1, planet2):

    # loc = EarthLocation.of_site('greenwich')

    for time in create_dates_generator(dates):
        with solar_system_ephemeris.set('jpl'):
            # yield get_body(planet1, time, loc).ra.value, get_body(planet2, time, loc).ra.value
            yield get_body(planet1, time).ra.value, get_body(planet2, time).ra.value


def get_right_ascensions(dates, planet1, planet2):

    nb_dates = len(dates)
    ra1 = np.zeros(nb_dates)
    ra2 = np.zeros(nb_dates)

    generator = create_right_ascension_generator(dates, planet1, planet2)

    for i, right_ascension in enumerate(generator):
        ra1[i] = right_ascension[0]
        ra2[i] = right_ascension[1]

    return ra1, ra2


def create_right_ascension_generator(dates, planet1, planet2):

    # loc = EarthLocation.of_site('greenwich')

    for time in create_dates_generator(dates):
        with solar_system_ephemeris.set('jpl'):
            # yield get_body(planet1, time, loc).ra.value, get_body(planet2, time, loc).ra.value
            yield get_body(planet1, time).ra.value, get_body(planet2, time).ra.value


def equatorial_coordinates(dates, body):

    # loc = EarthLocation.of_site('greenwich')

    for time in create_dates_generator(dates):
        with solar_system_ephemeris.set('jpl'):
            yield get_body(body, time).ra, get_body(body, time).dec


def get_longitudes(dates, body):

    nb_dates = len(dates)
    longitudes = np.zeros(nb_dates)

    coords = equatorial_coordinates(dates, body)

    # longitude begin = distance angulaire au point vernal

    coord1 = SkyCoord("0h0m0s", "0d0m0s", unit="deg")

    for i, coordsi in enumerate(coords):
        rai = coordsi[0]
        deci = coordsi[1]
        coordi = SkyCoord(rai, deci, unit="deg")
        if rai.value > 180:
            longitude = - coord1.separation(coordi).value
        else:
            longitude = coord1.separation(coordi).value
        longitudes[i] = longitude

    return longitudes
