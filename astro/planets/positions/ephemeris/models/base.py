# coding=utf-8
"""
Created on 2020, December 17th
@author: orion
"""
import pandas as pd

from astro.planets.positions.from_swiss_ephemeris import get_planet_dataframe
from astro.planets.positions.from_swiss_ephemeris import get_iflag

from astro.constants import QUADRANTIDES_BODIES, QUADRANTIDES_BODIES_COLORS


def get_bodies_data(bodies, dates):

    data = dict()

    for i, body in enumerate(bodies):
        data_frame = get_planet_dataframe(dates, body, get_iflag())

        zodiac = data_frame["zodiac"]
        is_retrograde = data_frame["is_retrograde"]
        data[body] = dict(
            # is_retrograde=is_retrograde,
            longitude=data_frame["longitude"],
            longitude_in_zodiac=data_frame["longitude_in_zodiac"],
            is_retrograde=is_retrograde,
            zodiac=zodiac,
            color=QUADRANTIDES_BODIES_COLORS[i],

        )

    return data


class Model(object):

    def __init__(self, start_date, end_date, freq, bodies, zodiac, output_type="html"):

        # initializations

        self.output_type = ""
        self.request = dict()
        self.data = dict()

        # settings
        self.data = dict(
            zodiac=zodiac,
        )
        self.output_type = output_type
        self.request = dict(
            date=dict(
                start=start_date,
                end=end_date,
                freq=freq,
            ),
            bodies=bodies,
        )

        self.load()

    def get_output_type(self):
        return self.output_type

    def get_request(self):
        return self.request

    def load_dates(self):
        dates = pd.date_range(
            start=self.request["date"]["start"],
            end=self.request["date"]["end"],
            freq=self.request["date"]["freq"],
        ).to_pydatetime()
        self.data["dates"] = dates

    def load(self):

        self.load_dates()
        self.data["bodies"] = get_bodies_data(QUADRANTIDES_BODIES, self.data["dates"])

    def get_data(self):
        return self.data
