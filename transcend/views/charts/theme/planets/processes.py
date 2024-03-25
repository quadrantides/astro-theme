# coding=utf-8
"""
Created on 2020, March 14th
@author: orion
"""
from transcend.views.graphics.components import Components as GraphicsComponents

from transcend.views.charts.theme.planets.aspects.processes import Process as AspectsProcess


# PLANETS

from transcend.views.charts.theme.planets.planets.charts import get_process_chart as get_planets_process_chart
from transcend.views.charts.theme.planets.planets.charts import get_view_chart as get_planets_view_chart

from transcend.views.charts.theme.planets.planets.processes import Process as ThemePlanetsProcess
from transcend.views.charts.theme.planets.planets.models import Model as ThemePlanetsModel

from transcend.views.charts.transit.planets.planets.processes import Process as TransitPlanetsProcess

from transcend.views.charts.theme.compounded.planets.planets.processes import Process as CompoundedPlanetsProcess
from transcend.views.charts.theme.compounded.planets.planets.models import Model as CompoundedPlanetsModel


class Process(GraphicsComponents):

    def __init__(
            self,
            process_model,
            show_aspects=True,
            show_points=True,
            show_annotations=True,
            graphics_dimensions=None,
    ):
        super(Process, self).__init__(process_model)
        self.show_aspects = show_aspects
        self.show_points = show_points
        self.show_annotations = show_annotations
        self.graphics_dimensions = graphics_dimensions
        self.points = dict()
        self.planets = dict()
        self.aspects = dict()
        self.process()

    def temp(self):

        self.planets = ThemePlanetsProcess(
            self.get_container().get_planets(),
            self.get_container().get_zodiac_angles(),
        )
        self.aspects = AspectsProcess(
            self.get_container().set_aspects(),
        )

    def get_zodiactype(self):
        chart_name = self.get_chart_name()
        sub_chart_name = self.get_sub_chart_name()
        if sub_chart_name:
            zodiactype = sub_chart_name
        else:
            zodiactype = chart_name
        return zodiactype

    def process(self):
        zodiactype = self.get_zodiactype()

        chart_name = self.get_chart_name()

        if chart_name == "compounded":
            # self.add_compounded_points()
            self.add_compounded_planets()
        else:
            # self.add_points(zodiactype)
            self.add_planets()

    def get_theme(self):
        return self.get_container().get_theme()

    def get_chart_name(self):
        return self.get_container().get_name()

    def get_sub_chart_name(self):
        return self.get_container().get_sub_name()

    def add_compounded_planets(self):
        tropical_process = self.add_planets(
            CompoundedPlanetsProcess,
            CompoundedPlanetsModel,
            load_only=True,
            sub_chart_name="tropical",
        )
        sidereal_process = self.add_planets(
            CompoundedPlanetsProcess,
            CompoundedPlanetsModel,
            load_only=True,
            sub_chart_name="sidereal",
        )

        tropical_process.create_graphics_components(
            # data=sidereal_process.get_chart().get_content()['planets'],
            data=sidereal_process,
        )

        components = tropical_process.get_graphics_components()

        self.add(components)

    def add_planets(self, load_only=False, sub_chart_name=''):
        theme = self.get_theme()
        if theme == "theme":
            process_model = ThemePlanetsProcess
            view_model = ThemePlanetsModel
        elif theme == "transit":
            process_model = TransitPlanetsProcess
            view_model = ThemePlanetsModel

        chart_name = self.get_chart_name()
        if not sub_chart_name:
            sub_chart_name = self.get_sub_chart_name()

        # if not sub_chart_name:
        #     # compounded CASE
        #     sub_chart_name = zodiactype

        data_model = self.get_container().get_content()
        process = process_model(
            data_model,
            get_planets_process_chart(
                theme,
                chart_name,
                sub_chart_name=sub_chart_name,
            ),
            # zodiac,
            view_model(
                get_planets_view_chart(
                    theme,
                    chart_name,
                    sub_chart_name=sub_chart_name,
                ),
                dimensions=self.graphics_dimensions,
            ),
            load_only=load_only,
            show_aspects=self.show_aspects,
            show_points=self.show_points,
            show_annotations=self.show_annotations,
            graphics_dimensions=self.graphics_dimensions,
        )
        if not load_only:
            self.add(
                process.get_graphics_components()
            )
        return process
