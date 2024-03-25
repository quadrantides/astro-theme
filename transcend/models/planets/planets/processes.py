# coding=utf-8
"""
Created on 2020, April 13th
@author: orion
"""
import math
import numpy as np
import copy

from django.utils.translation import ugettext as _

from transcend.constants import TRANSCEND_POINTS_OF_INTEREST
from transcend.containers import Container
from transcend.models.planets.structures import get_structure as get_planet_structure
from transcend.models.planets.planets.structures import get_planets_structure


class Process(Container):

    def __init__(self, data):
        super(Process, self).__init__(data)
        self.exclude = dict()
        self.data = []

    def process(self):
        planets = self.get_container()

        for key in planets.keys():
            data = copy.deepcopy(
                get_planet_structure()
            )
            data["label"] = key
            data["angle"] = planets[key]['angle']

            self.data.append(
                data,
            )

    def set_exclusions(self, points_of_interest=False):
        if points_of_interest:
            self.exclude["points_of_interest"] = points_of_interest
            # TRANSCEND_POINTS_OF_INTEREST

    def get_planet(self, label):
        data = self.get_data()
        nb_records = len(data)
        eod = False
        found = False
        i = 0
        while not eod and not found:
            if data[i]["label"] == label:
                found = True
            if not found:
                i += 1
                if i > nb_records - 1:
                    eod = True

        return data[i] if found else None

    def get_labels(self):
        labels = [data['label'] for data in self.get_data()]
        return labels

    def get_display_order(self, box_size):
        angles = []

        for planet in self.get_data():
            angles.append(
                planet['angle']
            )

        orders = list(range(len(angles)))

        sorted_indices = np.argsort(angles)

        orders = np.array(orders)
        angles = np.array(angles)

        angles = angles[sorted_indices]
        orders = orders[sorted_indices]

        dangle = angles[0] + 360 - angles[-1]
        i = 1
        while dangle < 2 * box_size:
            dangle = angles[i] - angles[i - 1]
            i += 1

        orders = np.roll(orders, -(i - 1))

        return orders.tolist()

    def get_data(self):
        points_of_interest_extraction = False
        some_extractions = False
        if self.exclude:
            points_of_interest_extraction = True if "points_of_interest" in self.exclude.keys() else False
            some_extractions = points_of_interest_extraction

        if some_extractions:
            data = []
            if points_of_interest_extraction:
                for datai in self.data:
                    if datai['label'] not in TRANSCEND_POINTS_OF_INTEREST:
                        data.append(datai)
        else:
            data = self.data

        return data

