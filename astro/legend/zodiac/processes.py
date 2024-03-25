# coding=utf-8
"""
Created on 2020, December 14th
@author: orion
"""
import copy
from transcend.processes import merge

from transcend.views.processes import Process as BaseProcess

from astro.views.traces.bars import get_shape as get_graphic_shape


def get_labels(labels, prefix):
    return ["{} - {}".format(prefix, label) for label in labels]


class Process(BaseProcess):

    def __init__(self, data_model, process_model, view_model):
        super(Process, self).__init__(
            data_model,
            copy.deepcopy(
                process_model,
            ),
            view_model,
        )

        self.process()

    def add_shape(self, x_range, y_range, color, reduce_opacity_factor=1.0):
        view_data = self.view_model.get_data().get_content()
        shape = copy.deepcopy(view_data['shape'])
        shape["opacity"] /= reduce_opacity_factor
        shape["x0"] = x_range[0]
        shape["x1"] = x_range[1]

        shape["y0"] = y_range[0]
        shape["y1"] = y_range[1]

        shape["fillcolor"] = color
        shape["line"]["color"] = shape["fillcolor"]

        data = self.get_chart().get_content()
        data['shapes'].append(shape)

    def load(self):
        model_data = self.container

        # db data model loading

        view_data = self.view_model.get_data().get_content()

        # ZODIAC data model adding

        data = self.get_chart().get_content()
        data = merge(
            view_data,
            data,
        )
        colors = view_data["colors"]["zodiac"]
        bg_colors = view_data["colors"]["background"]
        data['shapes'] = []

        for i, label in enumerate(model_data["zodiac"].keys()):

            begin = model_data["zodiac"][label]["begin"]["longitude"]
            end = model_data["zodiac"][label]["end"]["longitude"]

            if end < begin:
                y_ranges = [[begin, 360], [0, end]]
            else:
                y_ranges = [[begin, end]]

            color = colors[label]
            bg_color = bg_colors[label]

            for y_range in y_ranges:

                # shape header

                # x_range = model_data["graphic"]["zodiac_shape_xrange"]
                # self.add_shape(x_range, y_range, color)

                x_range = model_data["graphic"]["xaxis"]["range"]
                self.add_shape(x_range, y_range, bg_color, reduce_opacity_factor=1)

    def get_data(self):
        return self.data

    def create_shape_graphics_components(self, shape):

        graphic_shape = get_graphic_shape(shape)
        self.add_shapes([graphic_shape])

        # annotation = get_graphic_annotation(
        #     retrograde['annotation'],
        # )
        # self.add_annotations([annotation])

    def create_shapes_graphics_components(self, data=None):

        for shape in self.get_chart().get_content()['shapes']:
            self.create_shape_graphics_components(
                shape,
            )

    def create_graphics_components(self, data=None):
        self.create_shapes_graphics_components(data=data)
