# coding=utf-8
"""
Created on 2020, May 27th
@author: orion
"""
from transcend.models.openastro.models import SiderealDefault, TropicalDefault, OpenAstroInput
from transcend.views.charts.theme.processes import Process


def get_context(selection, json=True):

    process = Process(selection)
    return process.get_context(json=json)


def get_tropical_selection(theme, configuration, chart_name='', transit_date=None):
    selection = OpenAstroInput()
    selection.set_identifier(theme.get_person()["full_name"])
    selection.set_chart_name(chart_name)
    selection.set_zodiactype("tropical")
    selection.set_chartview("traditional")
    selection.set_postype("geo")
    selection.set_date(theme.date)
    selection.set_transit_date(transit_date)
    selection.set_timezonestr(theme.location.time_zone)
    selection.set_location(theme.location.city)
    selection.set_geolon(theme.location.longitude)
    selection.set_geolat(theme.location.latitude)

    selection.set_houses_system(configuration.houses_system.code)

    print("=========================== USER SELECTION BEGIN ======================================")
    zodiactype = "tropical"
    print()
    print(zodiactype.upper())
    current = selection.get_data()
    for key in current.keys():
        print(
            "{}:13 = {}".format(
                key,
                current[key],
            )
        )
    print()
    print("=========================== USER SELECTION END ========================================")

    return selection


def get_sidereal_selection(theme, configuration, chart_name='', transit_date=None):

    selection = OpenAstroInput()
    selection.set_identifier(theme.get_person()["full_name"])
    selection.set_chart_name(chart_name)
    selection.set_chartview("traditional")
    selection.set_postype("geo")
    selection.set_zodiactype("sidereal")

    selection.set_date(theme.date)
    selection.set_transit_date(transit_date)
    selection.set_timezonestr(theme.location.time_zone)
    selection.set_location(theme.location.city)
    selection.set_geolon(theme.location.longitude)
    selection.set_geolat(theme.location.latitude)

    selection.set_houses_system(configuration.houses_system.code)
    selection.set_sidereal_mode(configuration.mode.code)

    print("=========================== USER SELECTION BEGIN ======================================")
    zodiactype = "sidereal"
    print()
    print(zodiactype.upper())
    current = selection.get_data()
    for key in current.keys():
        print(
            "{}:13 = {}".format(
                key,
                current[key],
            )
        )
    print()
    print("=========================== USER SELECTION END ========================================")

    return selection


def get_default_tropical_selection(theme, configuration):
    selection = TropicalDefault()

    print("=========================== USER SELECTION BEGIN ======================================")
    zodiactype = "tropical (default)"
    print()
    print(zodiactype.upper())
    current = selection.get_data()
    for key in current.keys():
        print(
            "{}:13 = {}".format(
                key,
                current[key],
            )
        )
    print()
    print("=========================== USER SELECTION END ========================================")
    return selection


def get_openastro_data(selection):

    process = Process(selection)
    return process.get_context()


def get_context_graphics(context, configuration_tropical=None, configuration_sidereal=None, json=True):

    active_sidereal_configuration = configuration_sidereal.active if configuration_sidereal else False
    active_tropical_configuration = configuration_tropical.active if configuration_tropical else False

    selection = dict()
    if active_tropical_configuration:
        selection['tropical'] = \
            get_tropical_selection(context['theme'], configuration_tropical, transit_date=context['transit_date'])
    if active_sidereal_configuration:
        selection['sidereal'] = \
            get_sidereal_selection(context['theme'], configuration_sidereal, transit_date=context['transit_date'])

    context = dict()

    context.update(
        get_context(selection, json=json),
    )

    context['show'] = dict(
        tropical=active_tropical_configuration,
        sidereal=active_sidereal_configuration,
        compounded=active_tropical_configuration and active_sidereal_configuration,
    )

    return context


def get_context_graphics_data(theme, configuration_tropical=None, configuration_sidereal=None):

    active_sidereal_configuration = configuration_sidereal.active if configuration_sidereal else False
    active_tropical_configuration = configuration_tropical.active if configuration_tropical else False

    selection = dict()
    if active_tropical_configuration:
        selection['tropical'] = get_tropical_selection(theme, configuration_tropical)
    if active_sidereal_configuration:
        selection['sidereal'] = get_sidereal_selection(theme, configuration_sidereal)

    process = Process(selection)

    context = dict()

    context.update(
        process.get_graphics_data(),
    )

    context.update(
        process.get_cycles_data(),
    )

    context['show'] = dict(
        tropical=active_tropical_configuration,
        sidereal=active_sidereal_configuration,
        compounded=active_tropical_configuration and active_sidereal_configuration,
    )

    return context
