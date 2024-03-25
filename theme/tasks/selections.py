# coding=utf-8
"""
Created on 2020, May 26th
@author: orion
"""
from transcend.models.openastro.models import SiderealDefault, TropicalDefault, OpenAstroInput
from transcend.views.charts.theme.processes import Process


def get_openastro_data(selection):

    process = Process(selection)
    return process.get_context()


def load(theme, profile=None):

    print("=========================== USER SELECTION report ======================================")

    if profile:

        # sidereal

        sidereal_configuration = profile.get()['sidereal']

        if sidereal_configuration:
            sidereal = OpenAstroInput()
            sidereal.set_chartview("traditional")
            sidereal.set_postype("geo")
            sidereal.set_zodiactype("sidereal")

            sidereal.set_date(theme.date)
            sidereal.set_timezonestr(theme.time_zone)
            sidereal.set_location(theme.location.city)
            sidereal.set_geolon(theme.location.longitude)
            sidereal.set_geolat(theme.location.latitude)

            sidereal.set_houses_system(sidereal_configuration['houses_system'].code)
            sidereal.set_sidereal_mode(sidereal_configuration['mode'].code)

        else:
            sidereal = None

        tropical_configuration = profile.get()['tropical']

        if tropical_configuration:
            tropical = OpenAstroInput()
            tropical.set_zodiactype("tropical")
            tropical.set_chartview("traditional")
            tropical.set_postype("geo")
            tropical.set_date(theme.date)
            tropical.set_timezonestr(theme.location.time_zone)
            tropical.set_location(theme.location.city)
            tropical.set_geolon(theme.location.longitude)
            tropical.set_geolat(theme.location.latitude)

            tropical.set_houses_system(tropical_configuration['houses_system'].code)

        else:
            tropical = None

        selection = {

            'tropical': tropical,

            'sidereal': sidereal,

        }

    else:

        selection = {

            'tropical': TropicalDefault(),
            'sidereal': SiderealDefault(),

        }

    if selection['tropical']:
        zodiactype = "tropical"
        print()
        print(zodiactype.upper())
        current = selection[zodiactype].get_data()
        for key in current.keys():
            print(
                "{}:13 = {}".format(
                    key,
                    current[key],
                )
            )
        print()
    if selection['sidereal']:
        print()
        zodiactype = "sidereal"
        print(zodiactype.upper())
        current = selection[zodiactype].get_data()
        for key in current.keys():
            print(
                "{:13} = {}".format(
                    key,
                    current[key],
                )
            )
    print("=========================== USER SELECTION report ======================================")

    return get_openastro_data(selection)
