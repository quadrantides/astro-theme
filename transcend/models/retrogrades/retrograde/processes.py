# coding=utf-8
"""
Created on 2020, December 6th
@author: orion
"""
import pandas as pd
import numpy as np
import copy

from django.utils.translation import ugettext as _

from transcend.containers import Container
from transcend.models.retrogrades.retrograde.structures import get_structure as get_retrograde_structure
from astro.planets.positions.from_swiss_ephemeris import get_monotone_planet_dataframe
from astro.planets.positions.from_swiss_ephemeris import get_iflag
from astro.planets.positions.retrogrades.visualizations import get_retrograde_indexes


class Process(Container):

    def __init__(self, data):
        super(Process, self).__init__(data)
        self.exclude = dict()
        self.data = []

    def process(self):
        retrogrades = self.get_container()

        dates = pd.date_range(
            start=retrogrades["date"]["start"],
            end=retrogrades["date"]["end"],
            freq=retrogrades["date"]["freq"],
        ).to_pydatetime()

        data_frame = get_monotone_planet_dataframe(
            dates,
            retrogrades["body"],
            get_iflag(),
        )

        is_retrograde = data_frame["is_retrograde"].to_list()
        longitude = data_frame["longitude"].to_list()
        longitude_in_zodiac = data_frame["longitude_in_zodiac"].to_list()
        zodiac = data_frame["zodiac"].to_list()

        rindexes = get_retrograde_indexes(is_retrograde)
        nb_records = len(rindexes)
        i = 0
        istep = 1
        begin_rindex = rindexes[i]
        previous_rindex = begin_rindex

        i += istep
        eod = i >= nb_records

        while not eod:
            current_rindex = rindexes[i]
            j = i
            retrogradation_in_progress = (current_rindex - previous_rindex) == 1
            while not eod and retrogradation_in_progress:
                previous_rindex = current_rindex
                i += istep
                eod = i >= nb_records
                if not eod:
                    current_rindex = rindexes[i]
                    j = i
                    retrogradation_in_progress = (current_rindex - previous_rindex) == 1

            # rupture

            data = copy.deepcopy(
                get_retrograde_structure()
            )

            data["begin"]["date"] = dates[begin_rindex]
            data["begin"]["longitude"] = longitude[begin_rindex]
            data["begin"]["longitude_in_zodiac"] = longitude_in_zodiac[begin_rindex]
            data["begin"]["zodiac"] = zodiac[begin_rindex]

            data["end"]["date"] = dates[previous_rindex]

            data["end"]["longitude"] = longitude[previous_rindex]
            data["end"]["longitude_in_zodiac"] = longitude_in_zodiac[previous_rindex]
            data["end"]["zodiac"] = zodiac[previous_rindex]

            self.data.append(
                data,
            )

            # reinit for next retrograde

            previous_rindex = current_rindex
            begin_rindex = current_rindex

            i += 1
            eod = i >= nb_records

    def get_data(self):
        return self.data

