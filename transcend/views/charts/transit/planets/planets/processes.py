# coding=utf-8
"""
Created on 2020, August 12th
@author: orion
"""
from transcend.processes import merge

# THEME PLANETS

from transcend.views.charts.theme.planets.planets.processes import Process as ThemePlanetsProcess

from transcend.views.charts.theme.graphics.images import get_one as get_graphic_image
from transcend.views.charts.theme.graphics.planets.planets.traces import get_polar_segment as get_polar_graphic_segment
from transcend.views.charts.theme.graphics.planets.planets.annotations import get as get_graphic_annotation
from transcend.views.charts.theme.graphics.planets.planets.traces import get_polar_marker as get_polar_graphic_marker

# ASPECTS

from transcend.views.charts.transit.planets.planets.aspects.processes import Process as AspectsProcess
from transcend.views.charts.theme.planets.aspects.models import Model as AspectsModel

# GRADUATIONS

from transcend.views.charts.theme.graduations.processes import Process as GraduationsProcess
from transcend.views.charts.theme.planets.planets.graduations.models import Model as GraduationsModel


class Process(ThemePlanetsProcess):

    def __init__(
            self,
            data_model,
            chart,
            view_model=None,
            load_only=False,
            show_aspects=True,
            show_points=True,
            show_annotations=True,
            graphics_dimensions=None,
    ):
        super(Process, self).__init__(
            data_model,
            chart,
            view_model,
            load_only=load_only,
            show_aspects=show_aspects,
            show_points=show_points,
            show_annotations=show_annotations,
            graphics_dimensions=graphics_dimensions,
        )

    def load_graduations(self):
        self.processes['graduations'] = self.get_planets_graduations(
            GraduationsProcess,
            GraduationsModel,
            load_only=True,
            graphics_dimensions=self.graphics_dimensions,
        )

    # def load_points(self):
    #     pass

    def load_aspects(self):
        self.processes['aspects'] = self.get_aspects(
            AspectsProcess,
            AspectsModel,
            load_only=True,
        )

    def load(self):
        super(Process, self).load()

        zodiactype = self.get_zodiactype()

        data = self.get_chart().get_content()

        transit_planets_model = self.get_container().get_transit_planets(zodiactype)

        transit_planets = \
            transit_planets_model.get_data()

        if len(transit_planets) > 0:

            planets_structure = self.get_planets_structure(transit_planets_model)

            data['planets'] = planets_structure

    def get_planet(self, label):
        refs = self.get_chart().get_content()['planets']

        nb_refs = len(refs)
        eod = False
        found = False
        i = 0
        while not eod and not found:
            if refs[i]["label"] == label:
                found = True
            if not found:
                i += 1
                if i > nb_refs - 1:
                    eod = True

        if found:
            ref = refs[i]
        else:
            ref = None
        return ref

    # def get_data(self):
    #     return merge(
    #         self.legend.get_data(),
    #         self.get_chart().get_content(),
    #     )

    def create_planet_graphics_components(self, planet):

        self.add_traces(
            [
                get_polar_graphic_segment(
                    planet['line'],
                ),
                get_polar_graphic_marker(
                    planet['marker'],
                ),
            ]
        )
        annotation = get_graphic_annotation(
            planet['annotation'],
        )
        self.add_annotations([annotation])

        image = get_graphic_image(planet['image'])
        self.add_images([image])

    def create_planets_graphics_components(self, data=None):

        # if self.processes["aspects"]:
        #     clusters = self.processes["aspects"].get_container().get_conjunctions()
        #     print('ok')

        for planet in self.get_chart().get_content()['planets']:
            # if self.is_concerned_by_conjunction(planet["name"]):
            #     planet['image']['sizex'] *= 0.5
            #     planet['image']['sizey'] *= 0.5
            #     planet['annotation']['font']['size'] = 8

            self.create_planet_graphics_components(
                planet,
            )

    def create_graduations_graphics_components(self, data=None):
        if self.processes["graduations"]:

            self.processes["graduations"].create_graphics_components()
            components = self.processes["graduations"].get_graphics_components()
            self.add(components)

    # def create_points_graphics_components(self, data=None):
    #     pass

    def create_graphics_components(self, data=None):

        # self.create_points_graphics_components(data=data)
        self.create_graduations_graphics_components(data=data)

        self.create_planets_graphics_components(data=data)
        self.create_aspects_graphics_components(data=data)
