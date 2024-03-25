# coding=utf-8
"""
Created on 2020, April 30th
@author: orion
"""
import copy
from transcend.processes import merge

from transcend.views.processes import Process as BaseProcess

from transcend.views.charts.theme.graphics.planets.aspects.circle import get as get_graphic_circle


class Process(BaseProcess):

    def __init__(self, data_model, process_model, view_model=None):
        super(Process, self).__init__(
            data_model,
            process_model,
            view_model,
        )
        self.process()

    def load(self):

        view_data = self.view_model.get_data().get_content()
        data = self.get_chart().get_content()

        data = merge(
            view_data,
            data,
        )

    def create_graphics_components(self, data=None):
        trace = get_graphic_circle(
            self.get_chart().get_content(),
        )
        self.add_traces([trace])
