# coding=utf-8
"""
Created on 2020, March 18th
@author: orion
"""
import copy

from django.utils.translation import ugettext as _

from transcend.views.processes import Process as BaseProcess

from transcend.views.charts.theme.subtitles.constants import TITLE, TITLES_TO_BE_FRACTIONED
from transcend.views.charts.theme.graphics.subtitles import get as get_graphic_subtitle


class Process(BaseProcess):

    def __init__(self, data_model, process_data, theme_identifier, graphics_dimensions):
        super(Process, self).__init__(
            data_model,
            process_data,
        )
        self.theme_identifier = theme_identifier
        self.graphics_dimensions = graphics_dimensions
        self.process()

    def load(self):
        selection = self.get_container()["selection"]

        data = self.get_chart()
        # DATE

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "{} : {}".format(
            _("Theme"),
            self.theme_identifier,
        )

        data['chart']["theme"]['titles']['position']['top']['left']['theme identifier'] = title

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "{} : {} [ UTC ]".format(
            "Date",
            selection['date'],
        )

        data['chart']["theme"]['titles']['position']['top']['left']['date'] = title

        # LOCATION

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "{} : {}".format(
            _("City"),
            selection['location'],
        )

        data['chart']["theme"]['titles']['position']['top']['left']['location'] = title

        # LAT LON

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "Latitude / Longitude"

        data['chart']["theme"]['titles']['position']['top']['left']['latlon title'] = title

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "{} / {}".format(
            selection['latitude'],
            selection['longitude'],
        )

        data['chart']["theme"]['titles']['position']['top']['left']['latlon value'] = title

    def get_data(self):
        return self.get_chart().get_content()

    def create_graphics_components_for_position(self, position):

        annotations = []

        data = self.get_chart()

        titles = data['chart']["theme"]['titles']['position'][position[0]][position[1]]

        x0 = self.graphics_dimensions['title']['position'][position[0]][position[1]]['x0']
        y0 = self.graphics_dimensions['title']['position'][position[0]][position[1]]['y0']
        step = self.graphics_dimensions['title']['position'][position[0]][position[1]]['step']

        i = 0

        nb_title_char_max = 14

        for key in self.graphics_dimensions['title']['position'][position[0]][position[1]]['sorted_items']:
            if key in titles.keys():
                title = titles[key]['chart']['theme']['title']
                if title in TITLES_TO_BE_FRACTIONED.keys():
                    titlesi = TITLES_TO_BE_FRACTIONED[title]
                    for titlei in titlesi:
                        y = y0 - i * step
                        annotations.append(
                            get_graphic_subtitle(x0, y, titlei)
                        )
                        i += 1
                else:
                    y = y0 - i * step
                    annotations.append(
                        get_graphic_subtitle(x0, y, title)
                    )
                    i += 1

        return annotations

    def create_conjunctions_graphics_components(self):
        annotations = []

        x0 = self.graphics_dimensions['title']['position']['top']['right']['x0']
        y0 = self.graphics_dimensions['title']['position']['top']['right']['y0']
        step = self.graphics_dimensions['title']['position']['top']['right']['step']

        conjunctions = self.get_container()["conjunctions"]
        i = 0

        nb_conjunctions = len(conjunctions)
        if nb_conjunctions:
            y = y0 - i * step
            annotations.append(
                get_graphic_subtitle(x0, y, "Conjonctions:")
            )
            i += 2
            for conjunction in conjunctions:
                y = y0 - i * step
                annotations.append(
                    get_graphic_subtitle(x0, y, conjunction)
                )
                i += 1
        return annotations

    def create_graphics_components(self, data=None):
        annotations = self.create_graphics_components_for_position(['top', 'left'])
        self.add_annotations(annotations)
        # annotations = self.create_conjunctions_graphics_components()
        # self.add_annotations(annotations)
