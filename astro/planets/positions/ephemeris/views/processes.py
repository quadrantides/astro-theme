# coding=utf-8
"""
Created on 2020, December 17th
@author: orion
"""
import copy
from transcend.processes import merge

from astro.constants import BODIES_COLORS

from transcend.views.processes import Process as BaseProcess

from transcend.views.constants import PLANET_ICONS

from astro.planets.positions.ephemeris.views.structures import get_position_structure

from astro.planets.positions.ephemeris.views.traces import get_segment
from astro.constants import ZODIAC_NAMES


def get_bodies():
    bc = copy.deepcopy(BODIES_COLORS)
    bodies = list(bc.keys())
    bodies.remove("moon")
    return bodies


def get_body_color(body):
    return BODIES_COLORS[body]


class Process(BaseProcess):

    def __init__(
            self,
            data_model,
            chart,
            view_model=None,
            load_only=False,
            show_annotations=True,
            graphics_dimensions=None,
    ):
        super(Process, self).__init__(
            data_model,
            chart,
            view_model,
        )
        self.graphics_dimensions = graphics_dimensions
        self.legend = None
        self.show_annotations = show_annotations

        self.process(load_only=load_only)

    def get_source(self, key):
        if key not in PLANET_ICONS.keys():
            key = 'unknown'
        return PLANET_ICONS[key]

    # def add_legend(self, planets):
    #     self.legend = LegendProcess(
    #         planets,
    #     )

    def get_positions_structure(self, model):

        view_data = self.view_model.get_data().get_content()

        dates = model.get_data()["dates"]
        data = model.get_data()["bodies"]

        structures = []

        zodiac_offsets = dict()
        for i, zodiac in enumerate(ZODIAC_NAMES):
            zodiac_offsets[zodiac] = 30 * i

        for body in get_bodies():
            position_structure = get_position_structure()

            position_structure = merge(
                view_data,
                position_structure,
            )

            # marker adding

            position_structure['marker']["x"] = dates
            zodiac = data[body]['zodiac']
            longitude_in_zodiac = data[body]['longitude_in_zodiac']
            y = [l + zodiac_offsets[z] % 360 for l, z in zip(longitude_in_zodiac, zodiac)]
            position_structure['marker']["y"] = y

            position_structure['marker']['opacity'] = position_structure['opacity']
            position_structure['marker']['visible'] = position_structure['visible']
            position_structure['marker']['show_legend'] = position_structure['show_legend']
            position_structure['marker']['name'] = body
            position_structure['marker']['color'] = get_body_color(body)
            position_structure['marker']['custom_data'] = [
               [
                   position_structure['marker']['name'],

               ],
           ] * len(y)

            structures.append(
                position_structure
            )

        return structures

    def load(self):

        data = self.get_chart().get_content()

        model = self.get_container()

        structures = self.get_positions_structure(model)

        data['positions'] = structures

    def get_data(self):
        return merge(
            self.legend.get_data(),
            self.get_chart().get_content(),
        )

    def create_position_graphics_components(self, position):

        self.add_traces(
            [
                get_segment(
                    position['marker'],
                ),
            ]
        )

        # annotation = get_graphic_annotation(
        #     retrograde['annotation'],
        # )
        # self.add_annotations([annotation])

    def create_positions_graphics_components(self, data=None):

        for position in self.get_chart().get_content()['positions']:
            self.create_position_graphics_components(
                position,
            )

    def create_graphics_components(self, data=None):

        self.create_positions_graphics_components(data=data)
