# coding=utf-8
"""
Created on 2020, April 13th
@author: orion
"""
from transcend.containers import Container

from transcend.models.planets.points.processes import Process as PointsProcess
from transcend.models.planets.planets.processes import Process as PlanetsProcess
from transcend.models.planets.aspects.processes import Process as AspectsProcess


class Process(Container):

    def __init__(self, data):
        super(Process, self).__init__(data)

        # points of interest model

        self.points = dict(
        )

        # real planets model description

        self.planets = dict(
        )

        # real transit planets model description

        self.transit_planets = dict(
        )

        # aspects model description

        self.aspects = dict(
        )

        self.transit_aspects = dict(
        )

        self.data = dict()

    def set_planets(self, zodiactype):
        if zodiactype not in self.planets.keys():
            self.planets[zodiactype] = PlanetsProcess(
                self.get_container().get_planets()[zodiactype],
            )
            self.planets[zodiactype].process()

    def set_transit_planets(self, zodiactype):
        if zodiactype not in self.transit_planets.keys():
            self.transit_planets[zodiactype] = PlanetsProcess(
                self.get_container().get_transit_planets()[zodiactype],
            )
            self.transit_planets[zodiactype].process()

    def get_planets(self, zodiactype, exclude_points_of_interest=False):
        if zodiactype not in self.planets.keys():
            self.set_planets(zodiactype)
        self.planets[zodiactype].set_exclusions(points_of_interest=exclude_points_of_interest)
        return self.planets[zodiactype]

    def get_transit_planets(self, zodiactype, exclude_points_of_interest=False):
        if zodiactype not in self.transit_planets.keys():
            self.set_transit_planets(zodiactype)
        self.transit_planets[zodiactype].set_exclusions(points_of_interest=exclude_points_of_interest)
        return self.transit_planets[zodiactype]

    def set_points(self, zodiactype):
        if zodiactype not in self.points.keys():
            self.points[zodiactype] = PointsProcess(
                self.get_container().get_points()[zodiactype],
            )
            self.points[zodiactype].process()

    def get_points(self, zodiactype):
        if zodiactype not in self.points.keys():
            self.set_points(zodiactype)
        return self.points[zodiactype]

    def set_aspects(self, zodiactype):
        if zodiactype not in self.aspects.keys():
            self.aspects[zodiactype] = AspectsProcess(
                self.get_container().get_aspects()[zodiactype],
            )
            self.aspects[zodiactype].process()

    def get_aspects(self, zodiactype):
        if zodiactype not in self.aspects.keys():
            self.set_aspects(zodiactype)
        return self.aspects[zodiactype]

    def set_transit_aspects(self, zodiactype):
        if zodiactype not in self.transit_aspects.keys():
            self.transit_aspects[zodiactype] = AspectsProcess(
                self.get_container().get_transit_aspects()[zodiactype],
            )
            self.transit_aspects[zodiactype].process()

    def get_transit_aspects(self, zodiactype):
        if zodiactype not in self.transit_aspects.keys():
            self.set_transit_aspects(zodiactype)
        return self.transit_aspects[zodiactype]

    def get_tropical_zodiac(self):
        return self.get_container().get_tropical()['zodiac']

    def get_sidereal_zodiac(self):
        return self.get_container().get_sidereal()['zodiac']

    def get_data(self):
        return {
            'chart': {
                'points': self.points.get_data(),
                'planets': self.planets.get_data(),
                'aspects': self.aspects.get_data(),
            },
        }
