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

    planet1 = 'saturn'  # planète la plus lente
    planet2 = "jupiter"

    freq = '2Y'

    # angles = [60]
    # orbs = [4]

    orbs = [10, 8, 6, 4, 2]
    # orbs = [10]
    divisions = [5, 6, 8]

    angles = []
    for division in divisions:
        angles.extend(
            np.array(range(division)) * 360 / division,
        )
        angles.extend(
            (np.array(range(division)) * 360 / division) - 360,
        )

    angles = np.unique(angles)

    year = 1983
    nb_cycles = 1

    start = datetime.datetime(year, 1, 1, 0, 0)
    dates = pd.date_range(
        start=start,
        periods=nb_cycles + 1,
        freq=freq,
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

        loader.process(save=False)
        cycle = loader.get_cycle()
        cycle.visualize()
        print("ok")
