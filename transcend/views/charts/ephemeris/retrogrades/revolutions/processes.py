# coding=utf-8
"""
Created on 2020, December 8th
@author: orion
"""
import math
import numpy as np

from transcend.processes import merge

from transcend.constants import ANGLE_OFFSET

from transcend.views.processes import Process as BaseProcess

from transcend.views.charts.models.retrogrades.revolutions.structures import get_revolutions_structure

from transcend.views.charts.ephemeris.graphics.retrogrades.revolutions.traces import \
    get_polar_segment as get_polar_graphic_segment


class Process(BaseProcess):

    def __init__(self, data_model, process_model, view_model=None, load_only=False):
        super(Process, self).__init__(
            data_model,
            process_model,
            view_model,
        )
        self.legend = None
        self.process(load_only=load_only)

    def get_nb_revolutions(self, retrogrades):
        theta_max = retrogrades[0]["end"]["longitude"]
        for retrograde in retrogrades:
            theta_max = max(
                [theta_max, retrograde["begin"]["longitude"]],
            )

        return math.ceil(theta_max / 360)

    def get_spiral_coordinates(
            self,
            retrogrades_model,
    ):

        view_data = self.view_model.get_data().get_content()
        r_min = view_data["spiral"]['radius']["min"]
        r_max = view_data["spiral"]['radius']["max"]

        retrogrades = retrogrades_model.get_data()["chart"]["retrogrades"]

        nb_revolutions = self.get_nb_revolutions(retrogrades)

        theta_n = nb_revolutions * 360

        theta_0 = retrogrades[0]['end']['longitude']
        dtheta = theta_n - theta_0
        nb_degrees = int(dtheta)
        theta = ANGLE_OFFSET + theta_0 + nb_degrees * np.array(list(range(nb_degrees))) / (nb_degrees - 1)

        r = r_min + (r_max - r_min) * (1/(nb_revolutions * 360)) * abs(theta)

        return r, theta

    def get_revolutions_structure(self, retrogrades_model):

        view_data = self.view_model.get_data().get_content()

        r, theta = self.get_spiral_coordinates(retrogrades_model)

        revolutions_structure = get_revolutions_structure()

        revolutions_structure = merge(
            view_data,
            revolutions_structure,
        )

        revolutions_structure['line']['name'] = revolutions_structure['name']
        revolutions_structure['line']['opacity'] = revolutions_structure['opacity']
        revolutions_structure['line']['visible'] = revolutions_structure['visible']

        revolutions_structure['line']["angle"] = theta
        revolutions_structure['line']["radius"] = r

        return revolutions_structure

    def load(self):

        model = self.get_container()

        data = self.get_chart().get_content()

        data['revolutions'] = self.get_revolutions_structure(model)

    def get_data(self):
        return self.data

    def create_graphics_components(self, data=None):

        traces = [
            get_polar_graphic_segment(
                self.get_chart().get_content()['revolutions']["line"],
            ),
        ]

        self.add_traces(traces)

        components = self.get_graphics_components()

        self.add(components)
