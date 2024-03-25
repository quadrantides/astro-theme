# coding=utf-8
"""
Created on 2020, April 13th
@author: orion
"""
import copy
from transcend.containers import Container
from transcend.models.planets.structures import get_structure as get_point_structure
from transcend.models.planets.points.structures import get_points_structure


class Process(Container):

    def __init__(self, data):
        super(Process, self).__init__(data)
        self.data = dict()
        self.init()

    def init(self):
        pass

    def process(self):
        planets = self.get_container()

        self.data.update(
                copy.deepcopy(
                    get_points_structure(),
                ),
            )

        for key in planets.keys():
            data = copy.deepcopy(
                get_point_structure(),
            )
            data["label"] = key
            data["angle"] = planets[key]['angle']

            self.data["points"].append(
                data,
            )

    def get_data(self):
        return self.data
