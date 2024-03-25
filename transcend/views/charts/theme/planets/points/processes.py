# coding=utf-8
"""
Created on 2020, April 14th
@author: orion
"""
import math
import copy
from transcend.processes import merge
from transcend.views.processes import Process as BaseProcess
from transcend.views.charts.models.points.structures import get_structure as get_point_structure

from transcend.views.charts.theme.graphics.points.lines import get_all as get_graphic_lines
from transcend.views.charts.theme.graphics.points.annotations import get_all as get_graphic_annotations

from transcend.views.charts.theme.figure.processes import get_coordinates

A_AMPLITUDE = 40  # 35

ASC_SHIFT_AMPLITUDE = 50
OTHERS_SHIFT_AMPLITUDE = 0


def get_xshift_yshift(label, angle, shift=0):

    SHIFT_AMPLITUDE = ASC_SHIFT_AMPLITUDE if label[0:3] == "ASC" else OTHERS_SHIFT_AMPLITUDE

    xshift = SHIFT_AMPLITUDE * math.cos(((angle + shift) * math.pi) / 180)
    yshift = SHIFT_AMPLITUDE * math.sin(((angle + shift) * math.pi) / 180)

    return dict(
        xshift=xshift,
        yshift=yshift,
    )


def get_ax_ay(label, angle, shift=0):

    wax = A_AMPLITUDE * math.cos(((angle + shift) * math.pi) / 180)
    ax = - wax if label[0:3] == "ASC" else wax
    ay = - A_AMPLITUDE * math.sin(((angle + shift) * math.pi) / 180)

    return dict(
        ax=ax,
        ay=ay,
    )


def get_annotations_keywords(label, angle, shift=0):

    keywords = get_ax_ay(label, angle, shift=shift)
    keywords.update(
        get_xshift_yshift(label, angle, shift=shift)
    )
    return keywords


class Process(BaseProcess):

    def __init__(self, data_model, process_model, view_model=None, label_extension='', load_only=False, parent=None):
        super(Process, self).__init__(
            data_model,
            copy.deepcopy(
                process_model,
            ),
            view_model,
        )
        self.parent = parent
        self.label_extension = label_extension
        self.process(load_only=load_only)

    def process(self, load_only=False):
        super(Process, self).process(load_only=load_only)

    def get_label_extension(self):
        return self.label_extension

    def load(self):

        # db data model loading
        points = self.get_container().get_data()['points']

        # View model adding

        view_data = self.view_model.get_data().get_content()

        data = self.get_chart().get_content()

        for point in points:
            point_structure = copy.deepcopy(
                get_point_structure(),
            )

            point_structure = merge(
                view_data,
                point_structure,
            )

            point_structure = merge(
                point,
                point_structure,
            )

            point_structure['label'] = point_structure['label'].upper()

            point_structure['line']['angle'] = "" # point['angle']

            label = point_structure['label']
            if self.get_label_extension():
                label = "{}<sub>{}</sub>".format(
                    label,
                    self.get_label_extension()
                )

            point_structure['annotation']['text'] = label

            # if point_structure['label'] == "ASC":
            #     point_structure['line']["color"] = "#fff"

            point_structure['line']['points']['internal']['angle'] = point['angle']
            point_structure['line']['points']['external']['angle'] = point['angle']

            coordinates = get_coordinates(
                point_structure['angle'],
                point_structure['annotation']['radius'],
            )

            point_structure['annotation'] = merge(
                coordinates,
                point_structure['annotation'],
            )

            point_structure['annotation'] = merge(
                get_annotations_keywords(
                    point_structure['label'],
                    point['angle'],
                ),
                point_structure['annotation'],
            )

            if point_structure['label'] == "MC":
                point_structure['annotation']['showarrow'] = False

            # point_structure_angle = copy.deepcopy(
            #     get_point_structure(),
            # )
            #
            # point_structure_angle = merge(
            #     view_data,
            #     point_structure_angle,
            # )
            #
            # point_structure_angle = merge(
            #     point,
            #     point_structure_angle,
            # )
            #
            # elongation_degrees, angle_degree_minutes, elongation_degree_minutes_seconds, zodiac_label = self.parent.get_elongation(
            #     point["angle"])
            #
            # point_structure_angle['annotation']['text'] = ""  # angle_degree_minutes
            #
            # dangle = - 5 if point_structure['label'] == "MC" else 5
            #
            # coordinates = get_coordinates(
            #     point_structure_angle['angle'] + dangle,
            #     point_structure_angle['annotation']['radius'],
            # )
            #
            # point_structure_angle['annotation'] = merge(
            #     coordinates,
            #     point_structure_angle['annotation'],
            # )
            # point_structure_angle['annotation']["showarrow"] = False

            # data['points'].append([point_structure, point_structure_angle])
            data['points'].append(point_structure)

    def get_data(self):
        return self.data

    def create_graphics_components(self, data=None):

        traces = get_graphic_lines(self.get_chart().get_content()['points'])
        self.add_traces(traces)
        annotations = get_graphic_annotations(self.get_chart().get_content()['points'])
        self.add_annotations(annotations)
