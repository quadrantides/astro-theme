# coding=utf-8
"""
Created on 2020, March 18th
@author: orion
"""
import copy

from transcend.views.charts.theme.subtitles.processes import Process as BaseProcess
from transcend.views.charts.theme.subtitles.constants import TITLE


class Process(BaseProcess):

    def __init__(self, data_model, process_model):
        super(Process, self).__init__(
            data_model,
            copy.deepcopy(
                process_model,
            )
        )
        self.process()

    def load(self):

        tropical_selection = self.get_container().get_tropical_selection()
        sidereal_selection = self.get_container().get_sidereal_selection()

        # DATE

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "{} [ UTC ]".format(
                tropical_selection['date'],
        )

        self.get_chart()['chart']["theme"]['titles']['position']['top']['left']['date'] = title

        # LOCATION

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "{} - {}".format(
            tropical_selection['location'],
            tropical_selection['countrycode'],
        )

        self.get_chart()['chart']["theme"]['titles']['position']['top']['left']['location'] = title

        # LAT LON

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "Latitude / Longitude"

        self.get_chart()['chart']["theme"]['titles']['position']['top']['left']['latlon title'] = title

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "{} / {}".format(
            tropical_selection['latitude'],
            tropical_selection['longitude'],
        )

        self.get_chart()['chart']["theme"]['titles']['position']['top']['left']['latlon value'] = title

        # TROPICAL

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "{}".format(
            tropical_selection['zodiactype'].capitalize(),
        )

        self.get_chart()['chart']["theme"]['titles']['position']['bottom']['left']['tropical title'] = title

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "{}".format(
            tropical_selection['houses_system'][tropical_selection['houses_system_index']],
        )

        self.get_chart()['chart']["theme"]['titles']['position']['bottom']['left']['tropical houses_system'] = title

        # SIDEREAL

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "{}".format(
            sidereal_selection['zodiactype'].capitalize(),
        )

        self.get_chart()['chart']["theme"]['titles']['position']['bottom']['right']['sidereal title'] = title

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "{}".format(
            sidereal_selection['houses_system'][sidereal_selection['houses_system_index']],
        )

        self.get_chart()['chart']["theme"]['titles']['position']['bottom']['right']['sidereal houses_system'] = title

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "{}".format(
            sidereal_selection['sidereal_modes'][sidereal_selection['sidereal_mode_index']],
        )

        self.get_chart()['chart']["theme"]['titles']['position']['bottom']['right']['sidereal mode'] = title

    def create_graphics_components(self, data=None):
        super(Process, self).create_graphics_components()
        annotations = self.create_graphics_components_for_position(['bottom', 'left'])
        self.add_annotations(annotations)
        annotations = self.create_graphics_components_for_position(['bottom', 'right'])
        self.add_annotations(annotations)
