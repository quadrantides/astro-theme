# coding=utf-8
"""
Created on 2020, September 30th
@author: orion
"""
import os
import datetime
import pandas as pd
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'astro.settings')
django.setup()

from astro.planets.positions.from_swiss_ephemeris import get_planet_dataframe
from astro.planets.positions.from_swiss_ephemeris import get_iflag
from astro.planets.positions.retrogrades.visualizations import create as create_planets_position_visualization
from astro.planets.positions.retrogrades.visualizations import create_colored_timeserie
from astro.constants import QUADRANTIDES_BODIES, QUADRANTIDES_BODIES_COLORS


if __name__ == '__main__':

    body = 'uranus'

    start = datetime.datetime(2019, 1, 1, 0, 0)
    end = datetime.datetime(2019, 12, 31, 0, 0)

    start = datetime.datetime(1950, 1, 1, 0, 0)
    end = datetime.datetime(2050, 12, 31, 0, 0)

    start = datetime.datetime(2021, 1, 1, 0, 0)
    end = datetime.datetime(2022, 1, 7, 0, 0)

    freq = '1D'
    # freq = '1H'

    dates = pd.date_range(
        start=start,
        end=end,
        freq=freq,
    ).to_pydatetime()

    is_retrograde = dict()

    color = []
    bodies = dict()

    for i, body in enumerate(QUADRANTIDES_BODIES):

        is_retrograde = get_planet_dataframe(dates, body, get_iflag())["is_retrograde"].to_list()
        longitude_in_zodiac = get_planet_dataframe(dates, body, get_iflag())["longitude_in_zodiac"].to_list()
        zodiac = get_planet_dataframe(dates, body, get_iflag())["zodiac"].to_list()
        bodies[body] = dict(
            is_retrograde=is_retrograde,
            longitude_in_zodiac=longitude_in_zodiac,
            zodiac=zodiac,
            color=QUADRANTIDES_BODIES_COLORS[i],

        )
    # create_planets_position_visualization(
    #     dates,
    #     is_retrograde,
    #     planet,
    # )
    create_colored_timeserie(
        dates,
        bodies,
    )
