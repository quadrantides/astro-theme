# coding=utf-8
"""
Created on 2020, December 16th
@author: orion
"""
import copy
from transcend.containers import Container
from transcend.models.zodiac.constants import STRUCTURE


class Model(Container):

    def __init__(self, data):
        super(Model, self).__init__(data)
        self.data = dict()
        self.process()

    def process(self):
        model = self.get_container()
        angles = model["angles"]

        self.data = copy.deepcopy(
            STRUCTURE
        )

        self.data['zodiac']['angles'] = angles
        self.data['zodiac']['labels'] = model["labels"]

    def get_angles(self):
        return self.data['zodiac']['angles']

    def get_labels(self):
        return self.data['zodiac']['labels']

    def get_data(self):
        return self.data
