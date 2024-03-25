# coding=utf-8
"""
Created on 2020, June 5th
@author: orion
"""
import os
import pandas as pd
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'astro.settings')
django.setup()

import numpy as np
import datetime

from aspects.loaders import Loader
from aspects.visualizations import aspects as visualizations


if __name__ == '__main__':

    planet1 = 'sun'
    planet2 = "venus"

    orbs = [10, 8, 6, 4, 2]
    # orbs = [10]
    divisions = [5, 6, 8]

    angles = []
    for division in divisions:
        angles.extend(
            180 - np.array(range(division)) * 360 / division,
        )

    # angles = [-135]
    angles = np.unique(angles)

    year0 = 1950
    nb_cycles = 70

    tests_request = False
    creation_request = not tests_request

    start = datetime.datetime(year0, 1, 1, 0, 0)
    dates = pd.date_range(
        start=start,
        periods=nb_cycles + 1,
        freq='19M',
    ).to_pydatetime()

    ends = dates[1::]

    for i in range(len(dates) - 1):

        start = dates[i]
        end = dates[i+1]

        loader = Loader(
            planet1,
            planet2,
            start,
            end,
            angles,
            orbs,
        )

        if creation_request:
            loader.process()

        elif tests_request:
            cycle = loader.get_cycle()
            cycle.visualize()


