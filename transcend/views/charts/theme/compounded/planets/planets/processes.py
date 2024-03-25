# coding=utf-8
"""
Created on 2020, April 29th
@author: orion
"""
import copy

from transcend.views.charts.theme.graphics.segments.traces import get_polar_segments as get_graphic_lines
from transcend.views.charts.theme.planets.planets.processes import Process as BaseProcess

# ASPECTS

from transcend.views.charts.theme.compounded.planets.aspects.processes import Process as AspectsProcess
from transcend.views.charts.theme.compounded.planets.aspects.models import Model as AspectsModel


# POINTS  OF INTEREST

# from transcend.views.charts.theme.compounded.planets.points.processes import Process as PointsProcess
# from transcend.views.charts.theme.compounded.planets.points.models import Model as PointsModel

# GRADUATIONS

from transcend.views.charts.theme.graduations.processes import Process as GraduationsProcess
from transcend.views.charts.theme.compounded.planets.planets.graduations.models import Model as GraduationsModel


hovertemplate = \
    "<i>%{customdata[2]}</i><br>" + \
    "<i> %{customdata[3]}</i><br>" + \
    "<i> %{customdata[1]}</i><br>" + \
    "<i>%{customdata[4]}</i><br>" + \
    "<br>" + \
    "<i>%{customdata[7]}</i><br>" + \
    "<i> %{customdata[8]}</i><br>" + \
    "<i> %{customdata[6]}</i><br>" + \
    "<i>%{customdata[9]}</i>"


class Process(BaseProcess):

    def __init__(self, data_model, process_model, view_model=None, load_only=True):
        super(Process, self).__init__(
            data_model,
            process_model,
            view_model=view_model,
            load_only=load_only,
        )

    def load_aspects(self):
        self.processes['aspects'] = self.get_aspects(
            AspectsProcess,
            AspectsModel,
            load_only=True,
        )

    # def load_points(self):
    #     self.processes['points'] = self.get_points(
    #         PointsProcess,
    #         PointsModel,
    #         label_extension=self.get_zodiactype()[0],
    #         load_only=True,
    #
    #     )

    def load_graduations(self):
        self.processes['graduations'] = self.get_planets_graduations(
            GraduationsProcess,
            GraduationsModel,
            load_only=True,
        )

    def create_differences_graphics_components(self, planet, ref):

        planet['line']['points']['external']['angle'] = ref['line']['points']['external']['angle']
        planet['line']['color'] = "#ff0066"

        return planet

    def update_customdata(self, planet, ref):
        ref_cusotmdata = copy.deepcopy(
            ref['marker']['customdata'][0],
        )
        ref['marker']['customdata'][0].extend(planet['marker']['customdata'][0])
        planet['marker']['customdata'][0].extend(ref_cusotmdata)
        ref['marker']['hovertemplate'] = hovertemplate
        planet['marker']['hovertemplate'] = hovertemplate

    def create_planets_graphics_components(self, data=None):
        if data:
            planets = data.get_chart().get_content()['planets']

            lines = []
            if planets:
                for planet in planets:
                    ref = self.get_planet(planet['label'])
                    self.update_customdata(planet, ref)
                    # if has_differences(planet, ref):
                    #     print('ok')
                    #     lines.append(
                    #         self.create_differences_graphics_components(planet, ref),
                    #     )
                if len(lines) > 0:
                    traces = get_graphic_lines(
                        lines,
                    )
                    self.add_traces(traces)

        for planet in self.get_chart().get_content()['planets']:
            self.create_planet_graphics_components(planet)

    def create_aspects_graphics_components(self, data=None):
        if self.processes["aspects"]:
            if data:
                self.processes["aspects"].create_graphics_components()
                components = self.processes["aspects"].get_graphics_components()

                self.add(components)

    def create_points_graphics_components(self, data=None):
        if self.processes["points"]:
            if data:
                self.processes["points"].create_graphics_components(
                    data=data.processes["points"].get_chart().get_content()['points'],
                )
                components = self.processes["points"].get_graphics_components()

                self.add(components)

    def create_graduations_graphics_components(self, data=None):
        if self.processes["graduations"]:
            if data:
                self.processes["graduations"].create_graphics_components()
                components = self.processes["graduations"].get_graphics_components()
                self.add(components)

    def create_graphics_components(self, data=None):

        self.create_planets_graphics_components(data=data)

        self.create_graduations_graphics_components(data=data)

        self.update_conjunction_aspects_position()
        self.create_aspects_graphics_components(data=data)

        self.create_points_graphics_components(data=data)
