# coding=utf-8
"""
Created on 2020, April 20th
@author: orion
"""
from transcend.views.graphics.components import Components as GraphicsComponents

from transcend.views.charts.transit.graphics.theme.constants import DIMENSIONS as transit_theme_dimensions

# ASPECTS

from transcend.views.charts.theme.planets.aspects.charts import get_process_chart as get_aspects_process_chart
from transcend.views.charts.theme.planets.aspects.charts import get_view_chart as get_aspects_view_chart

# POINTS OF INTEREST

from transcend.views.charts.theme.planets.points.charts import get_process_chart as get_points_process_chart
from transcend.views.charts.theme.planets.points.charts import get_view_chart as get_points_view_chart


# GRADUATIONS

from transcend.views.charts.theme.planets.planets.graduations.charts import get_process_chart \
    as get_graduations_process_chart
from transcend.views.charts.theme.planets.planets.graduations.charts import get_view_chart \
    as get_graduations_view_chart


class Process(GraphicsComponents):

    def __init__(self, data_model, chart, view_model=None):
        super(Process, self).__init__(data_model)
        self.view_model = None
        # self.data = dict()
        self.chart = chart
        self.view_model = view_model

    def get_chart(self):
        return self.chart

    # def set_data(self, data):
    #     self.data = data
    #
    # def get_data(self):
    #     return self.data

    def get_chart_name(self):
        return self.get_chart().get_name()

    def get_sub_chart_name(self):
        return self.get_chart().get_sub_name()

    def get_zodiactype(self):
        if self.get_chart().get_name() == 'compounded':
            zodiactype = self.get_chart().get_sub_name()
        else:
            zodiactype = self.get_chart().get_name()
        return zodiactype

    def get_zodiac(self):
        zodiac = None
        if self.get_zodiactype() == "tropical":
            zodiac = self.get_container().get_tropical_zodiac()
        elif self.get_zodiactype() == "sidereal":
            zodiac = self.get_container().get_sidereal_zodiac()
        return zodiac

    def get_aspects(self, process_model, view_model, load_only=False):
        theme = self.get_chart().get_theme()
        chart_name = self.get_chart_name()
        sub_chart_name = self.get_sub_chart_name()

        if theme == "theme":
            data_model = self.get_container().get_aspects(
                self.get_zodiactype(),
            )
            view_model_instance = view_model(
                get_aspects_view_chart(
                    theme,
                    chart_name,
                    sub_chart_name=sub_chart_name,
                ),
            )
        elif theme == "transit":
            data_model = self.get_container().get_transit_aspects(
                self.get_zodiactype(),
            )
            view_model_instance = view_model(
                get_aspects_view_chart(
                    theme,
                    chart_name,
                    sub_chart_name=sub_chart_name,
                ),
                dimensions=transit_theme_dimensions,
            )

        process = process_model(
            data_model,
            get_aspects_process_chart(
                theme,
                chart_name,
                sub_chart_name=sub_chart_name,
            ),
            # zodiac,
            view_model_instance,
            load_only=load_only,
        )
        return process

    def get_points(self, process_model, view_model, label_extension="", load_only=False):
        theme = self.get_chart().get_theme()
        chart_name = self.get_chart_name()
        sub_chart_name = self.get_sub_chart_name()

        data_model = self.get_container().get_points(
            self.get_zodiactype(),
        )
        process = process_model(
            data_model,
            get_points_process_chart(
                theme,
                chart_name,
                sub_chart_name=sub_chart_name,
            ),

            view_model(
                get_points_view_chart(
                    theme,
                    chart_name,
                    sub_chart_name=sub_chart_name,
                ),
            ),
            label_extension=label_extension,
            load_only=load_only,
            parent=self,
        )
        return process

    def get_planets_graduations(self, process_model, view_model, load_only=False, graphics_dimensions=None):
        theme = self.get_chart().get_theme()
        chart_name = self.get_chart_name()
        sub_chart_name = self.get_sub_chart_name()

        data_model = None

        process = process_model(
            data_model,
            get_graduations_process_chart(
                theme,
                chart_name,
                sub_chart_name=sub_chart_name,
            ),

            view_model(
                get_graduations_view_chart(
                    theme,
                    chart_name,
                    sub_chart_name=sub_chart_name,
                ),
                dimensions=graphics_dimensions,
            ),
            load_only=load_only,
        )
        return process

    def get_aspects_graduations(self, process_model, view_model):
        theme = self.get_chart().get_theme()
        chart_name = self.get_chart_name()
        sub_chart_name = self.get_sub_chart_name()

        data_model = None

        process = process_model(
            data_model,
            get_graduations_process_chart(
                theme,
                chart_name,
                sub_chart_name=sub_chart_name,
            ),

            view_model(
                get_graduations_view_chart(
                    theme,
                    chart_name,
                    sub_chart_name=sub_chart_name,
                ),
            ),
            load_only=True,
        )
        return process

    def process(self, load_only=False):
        self.load()
        if not load_only:
            self.create_graphics_components()

    def load(self):
        pass

    def create_graphics_components(self, data=None):
        pass
