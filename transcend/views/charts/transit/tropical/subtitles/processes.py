# coding=utf-8
"""
Created on 2020, August 26th
@author: orion
"""
import copy

from transcend.views.charts.theme.subtitles.constants import TITLE
from transcend.views.charts.theme.tropical.subtitles.processes import Process as BaseProcess
from transcend.views.charts.transit.graphics.transit.constants import DIMENSIONS


class Process(BaseProcess):

    def __init__(self, data_model, process_model, theme_identifier, transit_identifier):
        self.transit_identifier = transit_identifier
        super(Process, self).__init__(
            data_model,
            copy.deepcopy(
                process_model,
            ),
            theme_identifier,
            DIMENSIONS,
        )
        self.process()

    def load(self):
        super(Process, self).load()

        selection = self.get_container()['selection']

        data = self.get_chart()
        # DATE

        title = copy.deepcopy(
            TITLE,
        )

        title['chart']["theme"]['title'] = "{} [UTC]".format(
            "Transit : {}".format(
                self.transit_identifier,
            ),
        )

        self.get_chart()['chart']["theme"]['titles']['position']['top']['left']['transit identifier'] = title
