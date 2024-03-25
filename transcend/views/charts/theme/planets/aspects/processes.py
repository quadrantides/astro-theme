# coding=utf-8
"""
Created on 2020, April 30th
@author: orion
"""
from transcend.processes import merge

from transcend.views.processes import Process as BaseProcess

from transcend.views.charts.models.aspects.structures import get_structure as get_aspect_structure
from transcend.models.points.structures import get_polar_point_structure

from transcend.views.charts.theme.planets.aspects.legend.processes import Process as LegendProcess
from transcend.views.charts.theme.planets.aspects.constants import COLORS

# from transcend.views.charts.theme.graphics.planets.aspects.lines import get_markers as get_graphic_aspects_markers

from transcend.views.charts.theme.graphics.processes import get_segment_coordinates, get_circle_coordinates
from transcend.views.charts.theme.graphics.planets.aspects.lines import get as get_graphic_aspect_lines

# GRADUATIONS

from transcend.views.charts.theme.graduations.processes import Process as GraduationsProcess
from transcend.views.charts.theme.planets.aspects.graduations.models import Model as GraduationsModel

from aspects.constants import SORTED_ASPECTS


def get_planets_names(aspect):
    names = aspect['marker']['customdata'][0][0].split("-")
    return [name.lower() for name in names]


class Process(BaseProcess):

    def __init__(self, data_model, process_model, view_model=None, load_only=False):
        super(Process, self).__init__(
            data_model,
            process_model,
            view_model,
        )
        self.legend = None
        self.processes = dict(
            graduations=None,
        )
        self.process(load_only=load_only)

    def add_legend(self):
        self.legend = LegendProcess(
            self.get_chart().get_content(),
        )

    def load_graduations(self):
        self.processes['graduations'] = self.get_aspects_graduations(
            GraduationsProcess,
            GraduationsModel,
        )

    def remove(self, aspect):
        self.get_chart().get_content()['aspects'].remove(aspect)

    def set_conjunction(self, radii, angles):
        aspect_name = "conjunction"
        view_data = self.view_model.get_data().get_content()
        aspect_structure = get_aspect_structure()
        aspect_structure = merge(
            view_data,
            aspect_structure,
        )
        aspect_structure['name'] = aspect_name
        aspect_structure['marker']["name"] = aspect_structure["name"]
        aspect_structure["marker"]["color"] = COLORS[aspect_name]
        aspect_structure["marker"]["size"] = 1.25

        wangle = list(range(angles[0], angles[1] + 1))
        nb_wangle = len(wangle)
        radius = [radii[0]] * nb_wangle
        radius.extend(
            [radii[1]] * nb_wangle
        )
        radius.append(radii[0])
        angle = wangle.copy()
        wangle.reverse()
        angle.extend(
            wangle,
        )
        angle.append(angle[0])
        coordinates = dict(
            radius=radius,
            angle=angle,
        )
        aspect_structure['marker'] = merge(
            coordinates,
            aspect_structure['marker'],
        )

        self.get_chart().get_content()['aspects'].append(aspect_structure)

    def get_sorted_aspects(self):
        sorted_aspects = []
        aspects = self.get_chart().get_content()['aspects']

        for name in SORTED_ASPECTS:
            for aspect in aspects:
                if aspect['name'] == name:
                    sorted_aspects.append(aspect)
        return sorted_aspects

    def load(self):

        # graduations loading

        # self.load_graduations()

        # db data model loading
        aspects = self.get_container().get_data()['aspects']

        # View model adding

        view_data = self.view_model.get_data().get_content()

        data = self.get_chart().get_content()

        for item in aspects:
            aspect = item['aspect']
            aspect_name = aspect['type']['name']
            aspect_structure = get_aspect_structure()

            aspect_structure = merge(
                view_data,
                aspect_structure,
            )

            aspect_structure['name'] = aspect_name

            planet1 = aspect["planets"][0]
            planet2 = aspect["planets"][1]

            if planet1["angle"] < 0:
                planet1["angle"] += 360

            if planet2["angle"] < 0:
                planet2["angle"] += 360

            # initialize circle line

            aspect_structure["circle"]["opacity"] = aspect_structure["opacity"]
            aspect_structure["circle"]["name"] = aspect_structure["name"]
            aspect_structure["circle"]["visible"] = aspect_structure["visible"]

            # initialize markers

            # aspect_structure['marker']["opacity"] = aspect_structure["opacity"]
            aspect_structure['marker']["name"] = aspect_structure["name"]
            # aspect_structure['marker']["visible"] = aspect_structure["visible"]

            if aspect_name == 'conjunction':
                point = get_polar_point_structure()
                conjunction_radius = aspect_structure["circle"]['radius']
                point['radius'] = conjunction_radius

                angle = (planet2['angle'] + planet1['angle']) / 2.0
                point['angle'] = angle
                coordinates = get_circle_coordinates(
                    point,
                )
                aspect_structure['marker'] = merge(
                    coordinates,
                    aspect_structure['marker'],
                )
                aspect_structure['marker']['customdata'] = [
                    [
                        "{}-{}".format(
                            planet1['label'],
                            planet2['label'],
                        ),
                    ],
                ] * len(coordinates['radius'])

                aspect_structure["marker"]["color"] = COLORS[aspect_name]
                aspect_structure["marker"]["size"] = 1.25
            else:
            # if aspect_name != 'conjunction':
                point1 = get_polar_point_structure()
                point1['radius'] = aspect_structure["circle"]['radius']
                point1['angle'] = planet1['angle']

                point2 = get_polar_point_structure()
                point2['radius'] = aspect_structure["circle"]['radius']
                point2['angle'] = planet2['angle']

                coordinates = get_segment_coordinates(
                    point1,
                    point2,
                )
                center_index = int(len(coordinates['radius'])/2)
                coordinates['radius'] = [coordinates['radius'][center_index]]
                coordinates['angle'] = [coordinates['angle'][center_index]]

                if aspect_name == 'square' or aspect_name == 'trine' or aspect_name == 'sextile':
                    aspect_structure['marker'] = merge(
                        coordinates,
                        aspect_structure['marker'],
                    )
                    aspect_structure['marker']['customdata'] = [
                                                                   [
                                                                       "{}-{}".format(
                                                                           planet1['label'],
                                                                           planet2['label'],
                                                                       ),
                                                                   ],
                                                               ] * len(coordinates['radius'])

                    aspect_structure["marker"]["color"] = COLORS[aspect_name]

                    if aspect_name == 'square':
                        aspect_structure["marker"]["symbol"] = "square-open"
                    elif aspect_name == 'trine':
                        aspect_structure["marker"]["symbol"] = "triangle-up-open"
                    elif aspect_name == 'sextile':
                        aspect_structure["marker"]["symbol"] = "asterisk-open"

                if aspect_name == 'square':
                    dash = 'dot'
                elif aspect_name == 'sextile':
                    dash = "dot"
                else:
                    dash = "solid"

                customdata = "{}-{}-{}-{}-{}".format(
                    'aspect',
                    self.get_zodiactype(),
                    aspect_name,
                    planet1["label"].capitalize(),
                    planet2["label"].capitalize(),
                )
                aspect_structure['line']['name'] = aspect_name
                aspect_structure['line']['customdata'] = [customdata]

                aspect_structure['line']['line']['color'] = COLORS[aspect_name]

                aspect_structure['line']['line']['dash'] = dash

                aspect_structure['line']['points']['planet1']['angle'] = planet1['angle']
                aspect_structure['line']['points']['planet2']['angle'] = planet2['angle']

                aspect_structure['line']['points']['planet1']['label'] = planet1['label']
                aspect_structure['line']['points']['planet2']['label'] = planet2['label']

            data['aspects'].append(
                aspect_structure
            )

        # self.add_legend()

    def get_data(self):
        return merge(
            self.legend.get_data(),
            self.data,
        )

    def get_conjunctions(self):
        res = []
        for aspect in self.get_chart().get_content()['aspects']:
            if aspect['name'] == "conjunction":
                res.append(aspect)
        return res

    def get_cycles(self):
        cycles = dict()
        return cycles

    def create_graphics_components(self, data=None):

        traces = get_graphic_aspect_lines(
            self.get_sorted_aspects(),
        )

        # traces.append(
        #     get_graphic_aspects_circle(
        #         self.get_chart().get_content()['aspects'][0],
        #     )
        # )

        self.add_traces(traces)

        for process_name in self.processes.keys():

            if self.processes[process_name]:
                self.processes[process_name].create_graphics_components()
                components = self.processes[process_name].get_graphics_components()

                self.add(components)


