# coding=utf-8
"""
Created on 2020, December 14th
@author: orion
"""
import os
import datetime
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'astro.settings')
django.setup()

from astro.constants import QUADRANTIDES_BODIES

from astro.planets.positions.ephemeris.models.astrological import Model
from astro.planets.positions.ephemeris.views.astrological.graphics import Graphic


if __name__ == '__main__':

    start = datetime.datetime(2020, 12, 25, 0, 0)
    end = datetime.datetime(2022, 1, 8, 0, 0)

    # start = datetime.datetime(2007, 12, 18, 0, 0)
    # end = datetime.datetime(2008, 12, 18, 0, 0)

    freq = '6H'

    title = "Positions des planètes - Date début {} Date fin {}".format(
        start.year,
        end.year,
    )

    model = Model(start, end, freq, QUADRANTIDES_BODIES, zodiac_type="", output_type="html")
    graphic = Graphic(model, title)
