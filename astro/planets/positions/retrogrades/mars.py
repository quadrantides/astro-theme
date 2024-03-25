# coding=utf-8
"""
Created on 2020, September 30th
@author: orion
"""
import os
import datetime
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'astro.settings')
django.setup()

from astro.planets.positions.from_swiss_ephemeris import get_planet_dataframe
from astro.planets.positions.from_swiss_ephemeris import get_iflag
from astro.planets.positions.retrogrades.visualizations import get_retrograde_indexes
from astro.planets.positions.retrogrades.visualizations import get_hover_retrograde_period

from astro.views.retrogrades.models import Visualize


def get_retrograde_data(
    dates,
    body,
):
    data_frame = get_planet_dataframe(dates, body, get_iflag())

    is_retrograde = data_frame["is_retrograde"].to_list()
    longitude = data_frame["longitude"].to_list()
    longitude_in_zodiac = data_frame["longitude_in_zodiac"].to_list()
    zodiac = data_frame["zodiac"].to_list()

    rindexes = get_retrograde_indexes(is_retrograde)
    nb_records = len(rindexes)
    i = 0
    istep = 1
    begin_rindex = rindexes[i]
    jbegin = i
    previous_rindex = begin_rindex
    jprevious = jbegin
    i += istep
    eod = i >= nb_records

    data = dict(
        retrogrades=dict(
            begin=dict(
                date=[],
                longitude=[],
                longitude_in_zodiac=[],
                zodiac=[],
            ),
            end=dict(
                date=[],
                longitude=[],
                longitude_in_zodiac=[],
                zodiac=[],
            ),
        ),
    )

    while not eod:
        current_rindex = rindexes[i]
        j = i
        retrogradation_in_progress = (current_rindex - previous_rindex) == 1
        while not eod and retrogradation_in_progress:
            previous_rindex = current_rindex
            jprevious = j
            i += istep
            eod = i >= nb_records
            if not eod:
                current_rindex = rindexes[i]
                j = i
                retrogradation_in_progress = (current_rindex - previous_rindex) == 1

        # rupture

        begin_date = dates[begin_rindex]
        end_date = dates[previous_rindex]

        data["retrogrades"]["begin"]["date"].append(
            dates[begin_rindex],
        )
        data["retrogrades"]["begin"]["longitude"].append(
            longitude[begin_rindex],
        )
        data["retrogrades"]["begin"]["longitude_in_zodiac"].append(
            longitude[begin_rindex],
        )
        data["retrogrades"]["begin"]["zodiac"].append(
            zodiac[begin_rindex],
        )

        data["retrogrades"]["end"]["date"].append(
            dates[previous_rindex],
        )
        data["retrogrades"]["end"]["longitude"].append(
            longitude[previous_rindex],
        )
        data["retrogrades"]["end"]["longitude_in_zodiac"].append(
            longitude[previous_rindex],
        )
        data["retrogrades"]["end"]["zodiac"].append(
            zodiac[previous_rindex],
        )

        previous_rindex = current_rindex
        begin_rindex = current_rindex
        jprevious = j
        jbegin = j

        i += 1
        eod = i >= nb_records

    return data


if __name__ == '__main__':

    body = 'mars'
    body = 'venus'

    start = datetime.datetime(1990, 1, 1, 0, 0)
    end = datetime.datetime(2020, 12, 31, 0, 0)

    # start = datetime.datetime(2020, 1, 1, 0, 0)
    # end = datetime.datetime(2020, 12, 31, 0, 0)
    #
    # start = datetime.datetime(2020, 11, 11, 0, 0)
    # end = datetime.datetime(2020, 11, 11, 23, 59)

    freq = '1H'

    # get retrogradations

    # retrograde_data = get_retrograde_data(
    #     dates,
    #     body,
    # )

    Visualize(start, end, freq, body)
