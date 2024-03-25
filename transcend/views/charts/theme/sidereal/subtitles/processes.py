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
        super(Process, self).load()

        selection = self.get_container()['selection']

        data = copy.deepcopy(
            TITLE,
        )

        data['chart']["theme"]['title'] = "{}".format(
            selection['houses_system'][selection['houses_system_index']],
        )

        self.get_chart()['chart']["theme"]['titles']['position']['top']['left']['houses_system'] = data

        data = copy.deepcopy(
            TITLE,
        )

        data['chart']["theme"]['title'] = "{}".format(
            selection['sidereal_modes'][selection['sidereal_mode_index']],
        )

        self.get_chart()['chart']["theme"]['titles']['position']['top']['left']['mode'] = data
