# coding=utf-8
"""
Created on 2020, April 22th
@author: orion
"""
import copy
from transcend.processes import merge

from transcend.views.processes import Process as BaseProcess

from transcend.views.charts.theme.graphics.graduations import get as get_graphic_graduations


class Process(BaseProcess):

    def __init__(self, data_model, process_model, view_model=None, load_only=False):
        super(Process, self).__init__(
            data_model,
            copy.deepcopy(
                process_model,
            ),
            view_model,
        )
        self.process(load_only=load_only)

    def load(self):

        view_data = self.view_model.get_data().get_content()
        data = self.get_chart().get_content()

        merge(
            view_data,
            data,
        )
        print("ok")

    def create_graphics_components(self, data=None):
        traces = get_graphic_graduations(
            self.get_chart().get_content(),
        )
        self.add_traces(traces)

