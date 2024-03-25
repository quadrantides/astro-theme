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

from astro.utils import convert_degrees_minutes_seconds
from astro.planets.positions.from_swiss_ephemeris import get_planet_data
from astro.planets.positions.from_swiss_ephemeris import get_iflag, get_planet_index
from astro.constants import QUADRANTIDES_BODIES

from transcend.models.openastro.models import TropicalDefault, SiderealDefault
from transcend.openastro import openAstroInstance


if __name__ == '__main__':

    d = datetime.datetime(2020, 11, 11, 16, 56)

    selection = TropicalDefault()
    selection.set_date(d)

    openastro = openAstroInstance(
        selection.get_data(),
    )
    data = openastro.get_data()

    planets = sorted(data["planets"].keys())

    for planet in planets:
        label_degrees, angle_degree_minutes, label_degree_minutes_seconds, zodiac_label = \
            openastro.get_elongation(data["planets"][planet]['angle'])
        print(
            "{:13} {:10} {}".format(
                planet,
                label_degree_minutes_seconds,
                zodiac_label,
            ),
        )
