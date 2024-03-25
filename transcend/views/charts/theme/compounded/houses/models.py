# coding=utf-8
"""
Created on 2020, April 22th
@author: orion
"""
from transcend.processes import merge
from transcend.views.charts.graphics.constants import DIMENSIONS
from transcend.views.charts.theme.compounded.geometries.models import Model as BaseModel


class Model(BaseModel):

    def __init__(self, chart, sub_chart_name=""):
        super(Model, self).__init__(chart, sub_chart_name=sub_chart_name)
        self.init()

    def init(self):
        self.load()

    def load(self):

        chart = self.get_container()
        chart_name = chart.get_name()
        sub_chart_name = chart.get_sub_name()

        colors = DIMENSIONS[chart_name][sub_chart_name]['houses']['pie']['colors']

        lines_houses_bounds = self.get_houses_lines_bounds(zodiactype=sub_chart_name)

        rmax, rmin, domain = self.get_houses_pie_bounds(zodiactype=sub_chart_name)

        content = chart.get_content()

        structure = dict(
            opacity=0.75,
            visible=True,
            name="",
            line=dict(
                opacity=0.4,
                points=dict(
                    internal=dict(
                        radius=lines_houses_bounds["radius"]['min'],
                    ),
                    external=dict(
                        radius=lines_houses_bounds["radius"]['max'],
                    ),
                ),
                dash='solid',
                color="#444",
                width=1,
            ),
            pie=dict(
                domain=domain,
                hole=rmin,
                colors=colors,
                # textinfo='none',
                textinfo='label',
                hovertext='',
                # hovertext=' ',
                # hoverinfo='none',
                marker=dict(
                    line=dict(
                        width=1.0,
                        color="#888",
                    ),
                ),
                hoverinfo='label',
                hovertemplate="" +
                "%{label}<br>" +
                "<i>%{customdata[0]}</i>",
            ),
        )

        merge(
            structure,
            content,
        )

    def get_data(self):
        return self.get_container()
