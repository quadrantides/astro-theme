# coding=utf-8
"""
Created on 2020, June 12th
@author: orion
"""
import pandas as pd
import swisseph as swe

import numpy as np

from astro.constants import ZODIAC_NAMES
from astro.planets.positions.models import TimeSeries as PlanetsTimeSeries

DATE_FORMAT = "%Y-%m-%d %H:%M"

COLORS = {1: 'red', 6: 'blue', 8: 'green'}

IFLAG = swe.FLG_SWIEPH + swe.FLG_SPEED + swe.FLG_NOABERR + swe.FLG_NOGDEFL + swe.FLG_J2000


def get_iflag(default=IFLAG):
    # check for apparent geocentric (default), true geocentric, topocentric or heliocentric
    iflag = default
    # iflag += swe.FLG_EQUATORIAL

    # if postype == "truegeo":
    #     iflag += swe.FLG_TRUEPOS
    # elif postype == "topo":
    #     iflag += swe.FLG_TOPOCTR
    # elif postype == "helio":
    #     iflag += swe.FLG_HELCTR
    #
    # # sidereal
    # if zodiactype == "sidereal":
    #     iflag += swe.FLG_SIDEREAL
    return iflag


def get_planet_index(planet):
    index = -1
    if planet == "sun":
        index = swe.SUN
    elif planet == "mercury":
        index = swe.MERCURY
    elif planet == "venus":
        index = swe.VENUS
    elif planet == "mars":
        index = swe.MARS
    elif planet == "jupiter":
        index = swe.JUPITER
    elif planet == "saturn":
        index = swe.SATURN
    elif planet == "uranus":
        index = swe.URANUS
    elif planet == "neptune":
        index = swe.NEPTUNE
    elif planet == "pluto":
        index = swe.PLUTO
    elif planet == "true node":
        index = swe.TRUE_NODE
    elif planet == "osc. apogee":
        index = swe.OSCU_APOG
    elif planet == "chiron":
        index = swe.CHIRON
    elif planet == "Asc":
        index = swe.ASC
    elif planet == "Mc":
        index = swe.MC
    return index


def create_zodiac_data(planet_data):

    planet_longitude = planet_data[0]
    planet_latitude_speed = planet_data[1]

    longitude_in_zodiac = 999.9
    zodiac = ""
    is_retrograde = None

    for i, zodiac in enumerate(ZODIAC_NAMES):

        deg_low = float(i * 30)
        deg_high = float((i + 1) * 30)
        if planet_longitude >= deg_low:
            if planet_longitude <= deg_high:
                longitude_in_zodiac = planet_longitude - deg_low
                # if latitude speed is negative, there is retrograde
                is_retrograde = True if planet_latitude_speed < 0 else False
                break

    return zodiac, longitude_in_zodiac, is_retrograde


def get_planet_data(date, planet_index, iflag):

    jul_day_ut = swe.julday(date.year, date.month, date.day, date.hour)

    results, flag = swe.calc(jul_day_ut, planet_index, iflag)

    longitude = results[0]
    latitude = results[1]
    distance = results[2]
    latitude_speed = results[3]
    zodiac, longitude_in_zodiac, is_retrograde = create_zodiac_data([longitude, latitude_speed])

    return longitude, latitude, distance, zodiac, longitude_in_zodiac, is_retrograde


def create_planet_data_generator(dates, planet_index, iflag):

    for date in dates:
        yield get_planet_data(date, planet_index, iflag)


def get_planet_dataframe(dates, planet, iflag):

    planet_index = get_planet_index(planet)

    nb_dates = len(dates)
    longitudes = np.full(nb_dates, 999.9)
    latitudes = np.full(nb_dates, 999.9)
    distances = np.full(nb_dates, 999.9)
    are_retrograde = np.full(nb_dates, False)
    zodiac = [""] * nb_dates
    longitudes_in_zodiac = np.full(nb_dates, 999.9)

    generator = create_planet_data_generator(dates, planet_index, iflag)

    nb_trigonometric_loops = 0
    for i, planet_data in enumerate(generator):
        longitude = planet_data[0] + nb_trigonometric_loops * 360
        if i > 0:
            if abs(longitude - previous_longitude) >= 350:
                positive_sign = longitude - previous_longitude > 0
                if positive_sign:
                    nb_trigonometric_loops -= 1
                    longitude -= 360
                else:
                    # Cela signifie que la planète a bouclé un tour du cercle trigonométrique

                    nb_trigonometric_loops += 1
                    longitude += 360

        longitudes[i] = longitude
        latitudes[i] = planet_data[1]
        distances[i] = planet_data[2]
        zodiac[i] = planet_data[3]
        longitudes_in_zodiac[i] = planet_data[4]
        are_retrograde[i] = planet_data[5]

        previous_longitude = longitude

    if longitudes[0] > 180:
        longitudes = longitudes - 360
    data = dict(
        longitude=longitudes,
        latitude=latitudes,
        distance=distances,
        is_retrograde=are_retrograde,
        zodiac=zodiac,
        longitude_in_zodiac=longitudes_in_zodiac,
    )

    return pd.DataFrame(data, index=dates)


def get_monotone_planet_dataframe(dates, planet, iflag):

    planet_index = get_planet_index(planet)

    nb_dates = len(dates)
    longitudes = np.full(nb_dates, 999.9)
    latitudes = np.full(nb_dates, 999.9)
    distances = np.full(nb_dates, 999.9)
    are_retrograde = np.full(nb_dates, False)
    zodiac = [""] * nb_dates
    longitudes_in_zodiac = np.full(nb_dates, 999.9)

    # generator = create_planet_data_generator(dates, planet_index, iflag)
    #
    # for i, planet_data in enumerate(generator):
    #     longitudes[i] = planet_data[0]
    # print(longitudes.tolist()[0:100])

    generator = create_planet_data_generator(dates, planet_index, iflag)
    mean_move = 15
    nb_trigonometric_loops = 0
    for i, planet_data in enumerate(generator):
        longitude = planet_data[0] + nb_trigonometric_loops * 360
        if i > 0:
            # print("{} {}".format(previous_longitude, longitude))
            move = abs(longitude - previous_longitude)
            if longitude - previous_longitude < 0:
                # rupture
                if move > 5 * mean_move:
                    # Cela signifie que la planète a bouclé un tour du cercle trigonométrique
                    longitude += 360
                    nb_trigonometric_loops += 1
                else:
                    # Cela signifie que la planète a rétrogradé
                    pass

        longitudes[i] = longitude
        latitudes[i] = planet_data[1]
        distances[i] = planet_data[2]
        zodiac[i] = planet_data[3]
        longitudes_in_zodiac[i] = planet_data[4]
        are_retrograde[i] = planet_data[5]

        previous_longitude = longitude

    # print(longitudes.tolist()[0:100])
    if longitudes[0] > 180:
        longitudes = longitudes - 360
    data = dict(
        longitude=longitudes,
        latitude=latitudes,
        distance=distances,
        is_retrograde=are_retrograde,
        zodiac=zodiac,
        longitude_in_zodiac=longitudes_in_zodiac,
    )

    return pd.DataFrame(data, index=dates)


def validate_longitudes(planet1, dataframe_planet1, planet2, dataframe_planet2):
    # offset0 = dataframe_planet2["longitude"][0] - dataframe_planet1["longitude"][0]
    # new_offset = [180, 360]
    # offset = 360 * int(offset0 / 360.0)
    # if offset0 >= 180:
    #     # arr = [abs(offset0 - offset - new_offset[0]), abs(offset0 - offset - new_offset[1])]
    #     # min_index = np.argmin(arr)
    #     # offset += new_offset[min_index]
    #     # dataframe_planet2["longitude"] = dataframe_planet2["longitude"] - offset
    #     dataframe_planet2["longitude"] = dataframe_planet2["longitude"] - 360
    # elif offset0 <= -180:
    #     # arr = [abs(offset0 + offset + new_offset[0]), abs(offset0 + offset + new_offset[1])]
    #     # min_index = np.argmin(arr)
    #     # offset += new_offset[min_index]
    #     # dataframe_planet2["longitude"] = dataframe_planet2["longitude"] + offset
    #     dataframe_planet2["longitude"] = dataframe_planet2["longitude"] + 360
    #
    # return [dataframe_planet1, dataframe_planet2]
    dangle1 = dataframe_planet1["longitude"][-1] - dataframe_planet1["longitude"][0]
    dangle2 = dataframe_planet2["longitude"][-1] - dataframe_planet2["longitude"][0]
    # la planète la lplus rapide est celle qui a parcouru la distance angulaire la plus grande sur le même laps de temps

    if dangle1 > dangle2:
        return [planet1, planet2], [dataframe_planet1, dataframe_planet2]
    else:
        return [planet2, planet1], [dataframe_planet2, dataframe_planet1]


def get_data(dates, planet1, planet2, postype="geo", zodiactype='tropical'):

    """
    iflag
    #define SEFLG_JPLEPH         1L     // use JPL ephemeris
    #define SEFLG_SWIEPH         2L     // use SWISSEPH ephemeris, default
    #define SEFLG_MOSEPH         4L     // use Moshier ephemeris
    #define SEFLG_HELCTR         8L     // return heliocentric position
    #define SEFLG_TRUEPOS        16L     // return true positions, not apparent
    #define SEFLG_J2000          32L     // no precession, i.e. give J2000 equinox
    #define SEFLG_NONUT          64L     // no nutation, i.e. mean equinox of date
    #define SEFLG_SPEED3         128L     // speed from 3 positions (do not use it, SEFLG_SPEED is // faster and preciser.)
    #define SEFLG_SPEED          256L     // high precision speed (analyt. comp.)
    #define SEFLG_NOGDEFL        512L     // turn off gravitational deflection
    #define SEFLG_NOABERR        1024L     // turn off 'annual' aberration of light
    #define SEFLG_EQUATORIAL     2048L     // equatorial positions are wanted
    #define SEFLG_XYZ            4096L     // cartesian, not polar, coordinates
    #define SEFLG_RADIANS        8192L     // coordinates in radians, not degrees
    #define SEFLG_BARYCTR        16384L     // barycentric positions
    #define SEFLG_TOPOCTR      (32*1024L)     // topocentric positions
    #define SEFLG_SIDEREAL     (64*1024L)     // sidereal positions
    """

    dataframe_planet1 = get_planet_dataframe(dates, planet1, get_iflag())
    dataframe_planet2 = get_planet_dataframe(dates, planet2, get_iflag())

    # dfs = [dataframe_planet1, dataframe_planet2]
    planets, dfs = validate_longitudes(planet1, dataframe_planet1, planet2, dataframe_planet2)
    container = {
        "planets": planets,
        "dfs": dfs,
    }

    return PlanetsTimeSeries(container)
