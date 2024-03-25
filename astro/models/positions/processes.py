# coding=utf-8
"""
Created on 2020, December 14th
@author: orion
"""
import pandas as pd

from django.utils.translation import ugettext as _

from transcend.containers import Container

from astro.planets.positions.from_swiss_ephemeris import get_monotone_planet_dataframe
from astro.planets.positions.from_swiss_ephemeris import get_iflag


class Process(Container):

    def __init__(self, model):
        super(Process, self).__init__(model)

        self.data = dict()
        self.graphic = None
        self.process()

    def process(self):
        pass

    def get_data(self):
        return self.get_container()
