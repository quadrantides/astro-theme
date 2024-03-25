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


if __name__ == '__main__':

    planet = 'uranus'

    start = datetime.datetime(2020, 1, 1, 0, 0)
    end = datetime.datetime(2030, 12, 31, 0, 0)

    dates = pd.date_range(
        start=start,
        end=end,
        freq='1D',
    ).to_pydatetime()

    is_retrograde = get_planet_dataframe(dates, planet, get_iflag())["is_retrograde"].to_list()

    create_planets_position_visualization(
        dates,
        is_retrograde,
        planet,
    )
    y0 = 7
