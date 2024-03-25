# coding=utf-8
"""
Created on 2020, December 20th
@author: orion
"""
from astro.planets.positions.ephemeris.models.base import Model as Base

from astro.zodiac.astronomical.constants import get_data as get_zodiac


class Model(Base):

    def __init__(self, start_date, end_date, freq, bodies, output_type="html"):
        super(Model, self).__init__(
            start_date,
            end_date,
            freq,
            bodies,
            zodiac=get_zodiac(),
            output_type=output_type,
        )

    def get_zodiac_type(self):
        return self.zodiac_type
