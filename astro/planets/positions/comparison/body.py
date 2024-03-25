# coding=utf-8
"""
Created on 2020, December 20th
@author: orion
"""
import pandas as pd
from datetime import datetime

from astro.planets.positions.from_swiss_ephemeris import get_planet_dataframe
from astro.planets.positions.from_swiss_ephemeris import get_iflag

from astro.planets.positions.from_astropy import get_longitudes


if __name__ == '__main__':

    body = 'sun'

    freq = "1D"

    start = datetime(2020, 1, 1, 0, 0)
    end = datetime(2020, 12, 21, 0, 0)
    dates = pd.date_range(
        start=start,
        end=end,
        freq=freq,
    )
    begin = datetime.now()
    astropy_longitudes = get_longitudes(dates, body)
    end = datetime.now()
    duration = end - begin
    print("ASTROPY duration = {}".format(duration))

    begin = datetime.now()
    data_frame = get_planet_dataframe(dates, body, get_iflag())
    swe_longitudes = data_frame["longitude"].to_list()
    end = datetime.now()
    duration = end - begin
    print("SWISS EPHEREMIS duration = {}".format(duration))
    print("ok")


