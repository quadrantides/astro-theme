# coding=utf-8
"""
Created on 2020, April 17th
@author: orion
"""
import copy

from transcend.containers import Container
from transcend.models.planets.structures import get_structure as get_planet_structure
from transcend.models.planets.aspects.structures import get_aspect_structure, get_aspects_structure


class Process(Container):

    def __init__(self, data):
        super(Process, self).__init__(data)
        self.data = dict()
        self.process()

    def process(self):
        aspects = self.get_container()

        self.data = copy.deepcopy(
            get_aspects_structure(),
        )

        for model_aspect in aspects:
            aspect = copy.deepcopy(
                get_aspect_structure()
            )
            for i in range(2):
                planet = copy.deepcopy(
                    get_planet_structure()
                )
                planet['label'] = model_aspect['planets'][i]['label']
                planet['angle'] = model_aspect['angles'][i]
                aspect['aspect']['planets'].append(planet)

            aspect['aspect']['type'] = model_aspect['aspect']

            self.data["aspects"].append(
                aspect,
            )

    def get_conjunctions(self):
        res = []
        aspects = self.get_container()
        for aspect in aspects:
            if aspect['aspect']['name'] == "conjunction":
                res.append(aspect)
        return res

    def get_data(self):
        return self.data
