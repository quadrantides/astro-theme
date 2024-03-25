# coding=utf-8
"""
Created on 2020, December 19th
@author: orion
"""
import copy
from transcend.processes import merge

from astro.planets.positions.ephemeris.views.constants import DIMENSIONS

from transcend.views.charts.models.images.structures import get_structure as get_image_structure

from transcend.views.constants import ZODIAC_ICONS, ZODIAC_ICONS_SIZE
from transcend.views.charts.theme.graphics.images import get_all as get_graphic_images

from astro.legend.zodiac.processes import Process as Base


def get_labels(labels, prefix):
    return ["{} - {}".format(prefix, label) for label in labels]


def get_image_size(key):
    if key not in ZODIAC_ICONS_SIZE.keys():
        key = 'unknown'
    return ZODIAC_ICONS_SIZE[key]*0.9


class Process(Base):

    def __init__(self, data_model, process_model, view_model):
        super(Process, self).__init__(
            data_model,
            copy.deepcopy(
                process_model,
            ),
            view_model,
        )

    def get_source(self, key):
        return ZODIAC_ICONS[key]

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

        for i, label in enumerate(model_data["zodiac"].keys()):

            # Image Processing

            image = copy.deepcopy(
                get_image_structure()['image'],
            )
            image = merge(
                view_data['image'],
                image,
            )

            image['sizex'] *= get_image_size(label)
            image['sizey'] *= get_image_size(label)

            image['label'] = label
            image['name'] = label
            image['source'] = self.get_source(label)

            dy = model_data["zodiac"][label]["end"]["longitude"] - model_data["zodiac"][label]["begin"]["longitude"]
            y_center = - DIMENSIONS['layout']['yaxis']['range'][0] + model_data["zodiac"][label]["begin"]["longitude"] + dy / 2.0
            coordinates = dict(
                x=image['x'],
                y=y_center/(DIMENSIONS['layout']['yaxis']['range'][1] - DIMENSIONS['layout']['yaxis']['range'][0]),
            )

            image = merge(
                coordinates,
                image,
            )
            data['images'].append(
                image
            )

    def create_images_graphics_components(self, data=None):
        images = get_graphic_images(self.get_chart().get_content()['images'])
        self.add_images(images)

    def create_graphics_components(self, data=None):
        super(Process, self).create_graphics_components(data=data)
        self.create_images_graphics_components(data=data)
