# coding=utf-8
"""
Created on 2020, December 20th
@author: orion
"""
import copy
import numpy as np
from transcend.processes import merge

from astro.constants import BODIES_COLORS
from astro.planets.positions.constants import DIRECT_BODIES_COLORS
from astro.planets.positions.ephemeris.views.constants import DIMENSIONS

from astro.planets.positions.ephemeris.views.processes import Process as BaseProcess

from transcend.views.constants import PLANET_ICONS

from astro.planets.positions.ephemeris.views.structures import get_position_structure

from astro.planets.positions.ephemeris.views.traces import get_segment
from astro.constants import ZODIAC_NAMES

DATE_FORMAT = "%d %b %Y"
ACCURACY = 2


def get_source(key):
    if key not in PLANET_ICONS.keys():
        wkey = "unknown"
    else:
        wkey = key
    return PLANET_ICONS[wkey]


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

    def get_position_structure(self, model, body, zodiac_offsets, indexes, is_retrograde=False):

        size = 4 if is_retrograde else 1.5
        name = "{}-R".format(body.capitalize()) if is_retrograde else "{}-D".format(body.capitalize())
        name = body.capitalize()
        # name = "R".format(body.capitalize()) if is_retrograde else body.capitalize()
        view_data = self.view_model.get_data().get_content()
        position_structure = get_position_structure()

        position_structure = merge(
            view_data,
            position_structure,
        )
        dates = model.get_data()["dates"]
        data = model.get_data()["bodies"]

        if len(indexes) > 0:
            position_structure['marker']["x"] = dates[indexes]
            str_dates = [date.strftime(DATE_FORMAT) for date in dates[indexes]]

            zodiac = data[body]['zodiac'][indexes]
            longitude_in_zodiac = data[body]['longitude_in_zodiac'][indexes]
            y = [l + zodiac_offsets[z] % 360 for l, z in zip(longitude_in_zodiac, zodiac)]
            position_structure['marker']["y"] = [round(yi, ACCURACY) for yi in y]

            position_structure['marker']['opacity'] = position_structure['opacity']
            position_structure['marker']['visible'] = position_structure['visible']
            position_structure['marker']['show_legend'] = position_structure['show_legend']
            position_structure['marker']['name'] = name
            position_structure['marker']['color'] = get_body_color(body)
            position_structure['marker']['size'] = size
            direction = "Retrograd" if is_retrograde else "Direct"
            custom_data = [[date, "{} {}°".format(zodiac, round(long, ACCURACY)), direction] for date, zodiac, long in
                           zip(str_dates, zodiac, longitude_in_zodiac)]
            position_structure['marker']['custom_data'] = custom_data

        return position_structure

    def get_positions_structure(self, model):

        view_data = self.view_model.get_data().get_content()

        dates = model.get_data()["dates"]
        data = model.get_data()["bodies"]

        structures = []

        zodiac_offsets = dict()
        for i, zodiac in enumerate(ZODIAC_NAMES):
            zodiac_offsets[zodiac] = 30 * i

        for body in get_bodies():

            # all positions

            indexes = np.invert(data[body]['is_retrograde'])
            position_structure = self.get_position_structure(model, body, zodiac_offsets, indexes)
            position_structure['marker']['show_legend'] = False
            structures.append(
                position_structure,
            )

            # retrogrades positions

            is_retrograde = data[body]['is_retrograde']

            indexes = [i for i, item in enumerate(is_retrograde) if item]
            if len(indexes) > 0:
                position_structure = \
                    self.get_position_structure(model, body, zodiac_offsets, indexes, is_retrograde=True)
                position_structure['marker']["size"] = 5

                structures.append(
                    position_structure,
                )

        # timeline marker adding

        str_dates = [date.strftime(DATE_FORMAT) for date in dates]

        position_structure = get_position_structure()

        position_structure = merge(
            view_data,
            position_structure,
        )

        position_structure['marker']["x"] = dates
        # position_structure['marker']["y"] = [DIMENSIONS['layout']['yaxis']['range'][0]] * len(dates)
        position_structure['marker']["y"] = [-10] * len(dates)
        position_structure['marker']['opacity'] = position_structure['opacity']
        position_structure['marker']['visible'] = position_structure['visible']
        position_structure['marker']['show_legend'] = True
        position_structure['marker']['name'] = "Time Line"
        position_structure['marker']['color'] = "#000"
        position_structure['marker']['symbol'] = "square"
        position_structure['marker']['size'] = 5
        custom_data = []

        for i, str_date in enumerate(str_dates):
            ci = [str_date]
            for body in get_bodies():
                ci.append(
                    "{:^8} {:>12} {:5}°".format(
                        body,
                        data[body]['zodiac'][i],
                        round(data[body]['longitude_in_zodiac'][i], ACCURACY),
                    )
                )
            custom_data.append(ci)

        position_structure['marker']['custom_data'] = custom_data
        hover_template = ""
        for j in range(len(get_bodies())):
            if not j:
                hover_template += "%{customdata[" + "{}".format(j) + "]}<br><br>"
            else:
                hover_template += "%{customdata[" + "{}".format(j) + "]}<br>"
        position_structure['marker']['hovertemplate'] = hover_template
        structures.append(
            position_structure
        )

        return structures
