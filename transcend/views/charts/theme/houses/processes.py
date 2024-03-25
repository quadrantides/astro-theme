# coding=utf-8
"""
Created on 2020, April 22th
@author: orion
"""
import copy
from transcend.processes import merge

from transcend.views.processes import Process as BaseProcess
from transcend.models.houses.models import Model as HousesModel

from transcend.views.charts.models.houses.structures import get_structure as get_houses_structure
from transcend.views.charts.theme.figure.processes import get_coordinates, get_centers

from transcend.views.constants import HOUSES_ICONS

from transcend.views.charts.theme.graphics.houses.annotations import get_all as get_graphic_houses
from transcend.views.charts.theme.graphics.segments.traces import get_polar_segments as get_graphic_polar_segments

from transcend.views.charts.pie.processes import get_rotation as get_pie_rotation

from transcend.views.charts.theme.graphics.pie.traces import get_pie as get_graphic_traces


def get_labels(labels, prefix):
    return ["{} - {}".format(prefix, label) for label in labels]


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
        return HOUSES_ICONS[key]

    def load(self):

        model_data = self.get_container()

        # model = HousesModel(
        #     model_data,
        # )

        # db data model loading

        model_labels = model_data['labels']

        view_data = self.view_model.get_data().get_content()

        data = self.get_chart().get_content()

        annotation_keywords = view_data.pop('annotation')
        line_keywords = view_data.pop('line')

        # HOUSES data model adding

        data = merge(
            model_data,
            data,
        )

        # HOUSES view model adding

        data = merge(
            view_data,
            data,
        )

        angles = data['angles']
        labels = data['labels']

        # Pie Processing

        # data['pie'] = merge(
        #     model_data,
        #     data['pie'],
        # )
        # pie_angles = [int(round(pie_angle)) for pie_angle in data['pie']['angles']]
        #
        # data['pie']['values'] = get_pie_values(pie_angles)
        # data['pie']['rotation'] = get_pie_rotation(
        #     data['pie']['values'],
        #     data['pie']['angles'],
        # )
        #
        # data['pie']['opacity'] = data['opacity']
        # data['pie']['visible'] = data['visible']
        # data['pie']['name'] = data['name']
        #
        # if self.get_chart().get_name() == 'compounded':
        #     zodiactype = self.get_chart().get_sub_name()
        # else:
        #     zodiactype = self.get_chart().get_name()
        #
        # data['pie']['customdata'] = [
        #     [
        #         zodiactype.capitalize(),
        #     ],
        # ] * len(model_labels)

        centers = get_centers(
            angles,
        )

        for i, label in enumerate(labels):

            struct = get_houses_structure()

            struct['annotation'] = merge(
                annotation_keywords,
                struct['annotation'],
            )

            struct['annotation']['label'] = label
            coordinates = get_coordinates(
                centers[i],
                annotation_keywords['radius'],
            )

            struct['annotation'] = merge(
                coordinates,
                struct['annotation'],
            )

            # lines

            struct['line'] = merge(
                line_keywords,
                struct['line'],
            )
            angle = int(
                round(
                    angles[i],
                )
            )
            struct['line']['points']['internal']['angle'] = angle
            struct['line']['points']['external']['angle'] = angle

            # struct['line']['opacity'] = data['opacity']
            struct['line']['visible'] = data['visible']
            struct['line']['name'] = data['name']

            data['annotations'].append(
                struct
            )

    def get_data(self):
        return self.data

    def create_graphics_components(self, data=None):
        # trace = get_graphic_traces(self.get_chart().get_content()['pie'])
        # self.add_traces([trace])
        traces = get_graphic_polar_segments(self.get_chart().get_content()['annotations'])
        self.add_traces(traces)

        annotations = get_graphic_houses(self.get_chart().get_content())
        self.add_annotations(annotations)
