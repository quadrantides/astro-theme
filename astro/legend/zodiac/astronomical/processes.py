# coding=utf-8
"""
Created on 2020, December 19th
@author: orion
"""
import copy
import numpy as np
from transcend.processes import merge

from astro.legend.zodiac.traces import get_text as get_graphical_text

from astro.legend.zodiac.processes import Process as Base


def get_labels(labels, prefix):
    return ["{} - {}".format(prefix, label) for label in labels]


def get_text_infos(model_data):

    zodiac_names = model_data["zodiac"].keys()
    text = []
    y = []
    for name in zodiac_names:

        begin = model_data["zodiac"][name]["begin"]["longitude"]
        end = model_data["zodiac"][name]["end"]["longitude"]

        if end < begin:
            y_ranges = [[begin, 360], [0, end]]
        else:
            y_ranges = [[begin, end]]

        for y_range in y_ranges:
            dy = y_range[1] - y_range[0]
            text.append(name)
            y.append(y_range[0] + dy / 2.0)

    return text, y


class Process(Base):

    def __init__(self, data_model, process_model, view_model):
        super(Process, self).__init__(
            data_model,
            copy.deepcopy(
                process_model,
            ),
            view_model,
        )

    def load(self):
        super(Process, self).load()

        model_data = self.container

        # db data model loading

        view_data = self.view_model.get_data().get_content()

        # ZODIAC data model adding

        data = self.get_chart().get_content()
        data = merge(
            view_data,
            data,
        )

        # text
        text, y = get_text_infos(model_data)
        sindexes = np.argsort(y)
        data["marker"]["y"] = np.array(y)[sindexes]
        data["marker"]["text"] = np.array(text)[sindexes]
        data["marker"]["x"] = [model_data["graphic"]["text"]["x0"]] * len(y)

    def create_text_graphics_components(self, data=None):

        trace = get_graphical_text(
            self.get_chart().get_content()['marker']
        )
        self.add_traces([trace])

    def create_graphics_components(self, data=None):
        super(Process, self).create_graphics_components(data=data)
        self.create_text_graphics_components(data=data)
