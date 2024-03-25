# coding=utf-8
"""
Created on 2020, April 11th
@author: orion
"""
import copy
from transcend.containers import Container
from transcend.models.houses.constants import STRUCTURE
from transcend.processes import merge


class Model(Container):

    def __init__(self, data):
        super(Model, self).__init__(data)
        self.data = dict()
        self.process()

    def process(self):
        model = self.get_container()

        self.data = copy.deepcopy(
            STRUCTURE
        )

        self.data['houses'] = merge(
            model,
            self.data['houses'],
        )

    def get_angles(self):
        return self.data['houses']['angles']

    def get_labels(self):
        return self.data['houses']['labels']

    def get_data(self):
        return self.data
