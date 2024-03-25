# coding=utf-8
"""
Created on 2020, March 28th
@author: orion
"""
import copy

from transcend.processes import merge
from transcend.containers import Container

from transcend.views.charts.theme.planets.aspects.legend.constants import ASPECT_LEGEND_STRUCTURE, LEGEND_STRUCTURE
from transcend.views.charts.theme.planets.planets.legend.models import Model as LegendModel


class Process(Container):

    def __init__(self, data_model):
        super(Process, self).__init__(data_model)
        self.data = dict()
        self.view_model = dict()
        self.init()

    def init(self):
        self.view_model = LegendModel()
        self.process()

    def process(self):
        self.load()

    def load(self):

        self.data = copy.deepcopy(
            LEGEND_STRUCTURE,
        )

        # db data model loading

        model_data = self.get_container()['chart']['aspects']

        view_data = self.view_model.get_data()

        for zodiactype in model_data.keys():

            aspects = model_data[zodiactype]
            for aspect in aspects:
                data = copy.deepcopy(
                   ASPECT_LEGEND_STRUCTURE,
                )

                data['chart']['aspect']['legend'] = merge(
                    aspect,
                    data['chart']['aspect']['legend'],
                )
                data['chart']['aspect']['legend']['visible'] = view_data['chart']['planet']['legend']['visible']
                data['chart']['aspect']['legend']['radius'] = view_data['chart']['planet']['legend']['marker']['radius']

                self.data['chart']['aspects']['legend'][zodiactype].append(
                    data['chart']['aspect']['legend']
                )

    # def old_process(self):
    #     aspects = []
    #     model_aspects = self.model.get_aspects()
    #     for model_aspect in model_aspects:
    #         aspect = copy.deepcopy(
    #             ASPECT_STRUCTURE()
    #         )
    #         planets = []
    #         planets_location_found = [False, False]
    #         for i in range(2):
    #             planet = copy.deepcopy(
    #                 get_planet_struct()
    #             )
    #             planet['name'] = model_aspect["planets"][i]['name']
    #             if self.planets_process.is_real_planet(planet['name']):
    #                 location = self.planets_process.get_location(planet['name'])
    #                 if location:
    #                     planets_location_found[i] = True
    #                     planet['angle'] = get_planets_angles()[planet['name']]['angle']
    #                     planet['radius'] = self.chart_definition['radius']
    #
    #                 planets.append(planet)
    #
    #         if planets_location_found[0] and planets_location_found[1]:
    #             aspect['planets'] = planets
    #
    #             aspect['type'] = model_aspect['aspect']
    #             aspect['color'] = COLORS[model_aspect['aspect']['name']]
    #
    #             aspect['legend'] = "{} {} - {}".format(
    #                 model_aspect['aspect']['name'],
    #                 planets[0]['name'],
    #                 planets[1]['name'],
    #             )
    #             aspects.append(aspect)
    #
    #     self.aspects = aspects
    #
    # def get_aspects(self):
    #     return self.aspects

    def get_data(self):
        return self.data
