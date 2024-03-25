# coding=utf-8
"""
Created on 2020, Jan 13th
@author: orion
"""
import copy
from transcend.processes import merge

from transcend.views.charts.models.images.structures import get_structure as get_image_structure
from transcend.views.charts.models.segments.structures import get_polar_structure as get_segment_structure
from transcend.views.charts.theme.figure.processes import get_centers
from transcend.views.charts.theme.figure.processes import get_coordinates
from transcend.views.processes import Process as BaseProcess
from transcend.views.constants import ZODIAC_ICONS
from transcend.models.zodiac.models import Model as ZodiacModel

from transcend.views.charts.theme.graphics.pie.traces import get as get_graphic_traces
from transcend.views.charts.theme.graphics.images import get_all as get_graphic_images
from transcend.views.charts.pie.processes import get_rotation as get_pie_rotation


def get_pie_values(angles):

    values = []
    bound_min_angles = angles
    bound_max_angles = angles[1::]
    bound_max_angles.append(angles[0])

    for i, bound_min_angle in enumerate(bound_min_angles):
        bound_max_angle = bound_max_angles[i]
        if bound_max_angle <= bound_min_angle:
            bound_max_angle += 360

        size = bound_max_angle - bound_min_angle

        values.append(size)

    return values


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

    def get_source(self, key):
        return ZODIAC_ICONS[key]

    def load(self):
        model_data = self.container

        for i, angle in enumerate(model_data['angles']):
            model_data['angles'][i] = round(angle)

        # model = ZodiacModel(
        #     model_data,
        # )

        # db data model loading

        view_data = self.view_model.get_data().get_content()

        # if 'images' in view_data.keys():
        #     image_keywords = view_data.pop('image')

        # segment_keywords = view_data.pop('segment')

        # ZODIAC data model adding

        data = self.get_chart().get_content()

        data['pie'] = merge(
            view_data['pie'],
            data['pie'],
        )

        # Pie Processing

        data['pie'] = merge(
            model_data,
            data['pie'],
        )

        model_labels = model_data['labels']
        data['pie']['labels'] = [label.capitalize() for label in model_labels]

        data['pie']['values'] = get_pie_values(data['pie']['angles'])
        data['pie']['rotation'] = get_pie_rotation(
            data['pie']['values'],
            data['pie']['angles'],
        )

        # view model adding

        data['pie']['opacity'] = view_data['opacity']
        data['pie']['visible'] = view_data['visible']
        data['pie']['name'] = view_data['name']

        if self.get_chart().get_name() == 'compounded':
            zodiactype = self.get_chart().get_sub_name()
        else:
            zodiactype = self.get_chart().get_name()

        data['pie']['customdata'] = [
            [
                zodiactype.capitalize(),
            ],
        ] * len(model_labels)

        # Segments and Images Processing

        if 'images' in data.keys():
            centers = get_centers(
                data['pie']['angles'],
            )

        for i, label in enumerate(model_labels):

            # Segment Processing

            segment_structure = copy.deepcopy(
                get_segment_structure(),
            )

            segment_structure = merge(
                view_data['segment'],
                segment_structure,
            )
            # internal point

            segment_structure['points']['internal']['angle'] = data['pie']['angles'][i]
            segment_structure['points']['external']['angle'] = data['pie']['angles'][i]

            segment_structure['opacity'] = view_data['opacity']
            segment_structure['visible'] = view_data['visible']
            segment_structure['name'] = view_data['name']

            data['segments'].append(
                segment_structure,
            )

            # Image Processing

            if 'images' in data.keys():

                image = copy.deepcopy(
                    get_image_structure()['image'],
                )
                image = merge(
                    view_data['image'],
                    image,
                )
                image['label'] = label
                image['name'] = label
                image['source'] = self.get_source(label)

                coordinates = get_coordinates(
                    centers[i],
                    image['radius'],
                )
                image = merge(
                    coordinates,
                    image,
                )
                data['images'].append(
                    image
                )

    def get_data(self):
        return self.data

    def create_graphics_components(self, data=None):
        traces = get_graphic_traces(self.get_chart().get_content())
        self.add_traces(traces)
        if 'images' in self.get_chart().get_content().keys():
            images = get_graphic_images(self.get_chart().get_content()['images'])
            self.add_images(images)
