# coding=utf-8
"""
Created on 2020, June 12th
@author: orion
"""
import pandas as pd
from transcend.containers import Container
from transcend.models.houses.constants import STRUCTURE
from transcend.processes import merge


class TimeSeries(Container):

    def __init__(self, data):
        super(TimeSeries, self).__init__(data)
        self.data = dict()
        self.process()

    def process(self):
        pass

    def _get(self, label):
        planets = self.get_container()["planets"]
        dfs = self.get_container()["dfs"]
        index = dfs[0].index
        data = {
            planets[0] : dfs[0][label].to_list(),
            planets[1]: dfs[1][label].to_list(),
        }

        return pd.DataFrame(data, index=index)

    def get_longitudes(self):
        return self._get("longitude")

    def get_latitudes(self):
        return self._get("latitude")

    def get_distances(self):
        return self._get("distance")

    def get_data(self):
        return self.data
