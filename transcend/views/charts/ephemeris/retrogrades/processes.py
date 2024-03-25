# coding=utf-8
"""
Created on 2020, December 6th
@author: orion
"""
from transcend.views.graphics.components import Components as GraphicsComponents


# RETROGRADES

from transcend.views.charts.ephemeris.retrogrades.retrogrades.charts import \
    get_process_chart as get_retrogrades_process_chart

from transcend.views.charts.ephemeris.retrogrades.retrogrades.charts import \
    get_view_chart as get_retrogrades_view_chart

from transcend.views.charts.ephemeris.retrogrades.retrogrades.processes import Process as RetrogradesProcess
from transcend.views.charts.ephemeris.retrogrades.retrogrades.models import Model as RetrogradesModel


class Process(GraphicsComponents):

    def __init__(
            self,
            process_model,
            show_annotations=True,
            graphics_dimensions=None,
    ):
        super(Process, self).__init__(process_model)
        self.show_annotations = show_annotations
        self.graphics_dimensions = graphics_dimensions
        self.process()

    def process(self):
        self.add_retrogrades()

    def get_theme(self):
        return self.get_container().get_theme()

    def get_chart_name(self):
        return self.get_container().get_name()

    def add_retrogrades(self, load_only=False):
        theme = self.get_theme()
        process_model = RetrogradesProcess
        view_model = RetrogradesModel

        chart_name = self.get_chart_name()

        data_model = self.get_container().get_content()
        process = process_model(
            data_model,
            get_retrogrades_process_chart(
                theme,
                chart_name,
            ),
            # zodiac,
            view_model(
                get_retrogrades_view_chart(
                    theme,
                    chart_name,
                ),
                dimensions=self.graphics_dimensions,
            ),
            load_only=load_only,
            show_annotations=self.show_annotations,
            graphics_dimensions=self.graphics_dimensions,
        )
        if not load_only:
            self.add(
                process.get_graphics_components()
            )
        return process
