# coding=utf-8
"""
Created on 2020, December 17th
@author: orion
"""
from astro.zodiac.astrological.constants import get_data as get_zodiac
from astro.planets.positions.ephemeris.models.base import Model as Base


class Model(Base):

    def __init__(self, start_date, end_date, freq, bodies, output_type="html", zodiac_type="tropical"):
        super(Model, self).__init__(
            start_date,
            end_date,
            freq,
            bodies,
            zodiac=get_zodiac(),
            output_type=output_type,
        )
        # initializations

        self.zodiac_type = ""

        # settings

        self.zodiac_type = zodiac_type

    def get_zodiac_type(self):
        return self.zodiac_type
