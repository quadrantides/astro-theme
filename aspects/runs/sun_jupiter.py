# coding=utf-8
"""
Created on 2020, June 22th
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


if __name__ == '__main__':

    planet1 = 'sun'
    planet2 = "jupiter"

    orbs = [10, 8, 6, 4, 3, 2]
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

    year0 = 1947
    freq = '243D'
    nb_cycles = 10

    start = datetime.datetime(year0, 3, 2, 0, 0)
    dates = pd.date_range(
        start=start,
        periods=nb_cycles + 1,
        freq=freq,
    ).to_pydatetime()

    ends = dates[1::]

    # for i in range(len(dates) - 1):
    #
    #     start = dates[i]
    #     end = dates[i+1]
    #
    #     loader = Loader(
    #         planet1,
    #         planet2,
    #         start,
    #         end,
    #         angles,
    #         orbs,
    #     )
    #
    #     loader.process(save=False)

    start = datetime.datetime(1946, 11, 21, 0, 0)
    end = datetime.datetime(1954, 2, 15, 0, 0)

    loader = Loader(
        planet1,
        planet2,
        start,
        end,
        angles,
        orbs,
    )

    loader.process(save=False)
