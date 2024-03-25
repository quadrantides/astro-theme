# coding=utf-8
"""
Created on 2020, December 20th
@author: orion
"""
import copy
from transcend.processes import merge

from astro.constants import BODIES_COLORS

from astro.planets.positions.ephemeris.views.processes import Process as BaseProcess
from astro.planets.positions.ephemeris.views.structures import get_position_structure

from astro.constants import ZODIAC_NAMES

DATE_FORMAT = "%d/%m/%Y"


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
            load_only=load_only,
            show_annotations=show_annotations,
            graphics_dimensions=graphics_dimensions,
        )

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
            str_dates = [date.strftime(DATE_FORMAT) for date in dates]
            zodiac = data[body]['zodiac']
            position_structure['marker']["y"] = [round(longitude) for longitude in data[body]['longitude']]

            position_structure['marker']['opacity'] = position_structure['opacity']
            position_structure['marker']['visible'] = position_structure['visible']
            position_structure['marker']['show_legend'] = position_structure['show_legend']
            position_structure['marker']['name'] = body
            position_structure['marker']['color'] = get_body_color(body)
            position_structure['marker']['custom_data'] = [items for items in zip(str_dates, position_structure['marker']["y"], data[body]['zodiac'])]

            structures.append(
                position_structure
            )

        return structures
