# coding=utf-8
"""
Created on 2020, March 27th
@author: orion
"""
import copy

from transcend.processes import merge

from transcend.views.constants import PLANET_ICONS
from transcend.views.charts.theme.images import get as get_image
from transcend.views.charts.theme.planets.planets.legend.models import Model as LegendModel
from transcend.views.charts.theme.planets.planets.legend.constants import PLANET_LEGEND_STRUCTURE
from transcend.views.charts.theme.planets.planets.legend.constants import LEGEND_STRUCTURE
from transcend.views.charts.theme.planets.planets.legend.constants import POSITIONS
from transcend.views.charts.theme.planets.planets.legend.constants import get_text_position


class Process(object):

    def __init__(self, planets):
        self.next_free_position = 0
        self.planets = []
        self.view_model = dict()
        self.data = dict()
        self.init(planets)

    def init(self, planets):
        self.planets = planets
        self.view_model = LegendModel()
        self.init_next_position()
        self.process()

    def init_next_position(self):
        self.next_free_position = len(self.planets) - len(POSITIONS.keys()) + 1

    def process(self):
        self.load()

    def get_angles(self):
        res = dict()
        nb_planets = len(self.planets)
        for planet in self.planets:
            position = self.get_position(planet)
            res[planet] = {'angle': position * 360 / nb_planets}

        return res

    def get_position(self, planet):
        res = self.next_free_position
        if planet in POSITIONS.keys():
            res = POSITIONS[planet]
        else:
            self.next_free_position += 1
        return res

    def get_source(self, key):
        if key not in PLANET_ICONS.keys():
            wkey = "unknown"
        else:
            wkey = key
        return PLANET_ICONS[wkey]

    def load(self):

        self.data = copy.deepcopy(
            LEGEND_STRUCTURE,
        )
        planets = self.planets

        angles = self.get_angles()

        view_data = self.view_model.get_data()
        image_keywords = view_data['chart']['planet']['legend'].pop('image')

        for planet in planets:

            data = copy.deepcopy(
                PLANET_LEGEND_STRUCTURE,
            )
            label = planet
            angle = angles[planet]["angle"]
            data["chart"]['planet']['legend']['label'] = label
            data["chart"]['planet']['legend']['angle'] = angle

            data = merge(
                view_data,
                data,
            )
            source = self.get_source(planet)

            image = get_image(angle, label, source, image_keywords)
            data['chart']['planet']['legend']['image'] = image
            data['chart']['planet']['legend']['text']['position'] = get_text_position(angle)

            self.data['chart']['planets']['legend'].append(
                data['chart']['planet']['legend']
            )

    def get_data(self):
        return self.data
