# coding=utf-8
"""
Created on 2020, June 5th
@author: orion
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'astro.settings')
django.setup()

import pandas as pd
from datetime import datetime


from astro.planets.positions.from_astropy import get_right_ascensions as get_astropy_right_ascensions
from astro.planets.positions.from_swiss_ephemeris import get_data as get_swe_data
from astro.planets.positions.visu import compare

if __name__ == '__main__':

    planet1 = 'sun'
    planet2 = "venus"

    years = [1950]
    period = 1  # in years

    freq = "1D"

    for year in years:

        start = datetime(year, 12, 21, 0, 0)
        end = datetime(year + period, 12, 20, 0, 0)
        dates = pd.date_range(
            start=start,
            end=end,
            freq=freq,
        )
        begin = datetime.now()
        astropy_ras = get_astropy_right_ascensions(dates, planet1, planet2)
        # print("SWE ascensions droites = {}".format(astropy_ras))
        end = datetime.now()
        duration = end - begin
        print("ASTROPY duration = {}".format(duration))

        begin = datetime.now()
        swe_longitudes = get_swe_data(dates, planet1, planet2).get_longitudes()
        # print("SWE Longitudes = {}".format(swe_longitudes))
        end = datetime.now()
        duration = end - begin
        print("SWISS EPHEREMIS duration = {}".format(duration))

        compare(dates, planet1, planet2, swe_longitudes, astropy_ras)
