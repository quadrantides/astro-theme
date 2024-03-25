# coding=utf-8
"""
Created on 2020, April 28th
@author: orion
"""
from transcend.processes import merge
from transcend.views.charts.theme.constants import WHEEL
from transcend.views.charts.theme.compounded.geometries.models import Model as BaseModel


class Model(BaseModel):

    def __init__(self, chart, sub_chart_name=""):
        super(Model, self).__init__(chart, sub_chart_name=sub_chart_name)
        self.init()

    def init(self):
        self.load_chart()

    def load_chart(self):
        chart = self.get_container()
        sub_chart_name = chart.get_sub_name()

        points_bounds = self.get_points_lines_bounds(zodiactype=sub_chart_name)['radius']

        external_radius = WHEEL['houses']['lines']['radius']['external']
        annotation_radius = external_radius

        content = chart.get_content()

        color = WHEEL["points"]['line']['color']

        structure = dict(
            opacity=0.65,
            visible=True,
            name="point of interest [ASC or MC",
            annotation=dict(
                radius=annotation_radius,
                xanchor="center",
                yanchor="middle",
                font=dict(
                    color=color,
                    size=15,
                ),
                arrowcolor=color,
                showarrow=True,
                showtext=True,
            ),
            line=dict(
                points=dict(
                    internal=dict(
                        radius=points_bounds["min"],
                    ),
                    external=dict(
                        radius=points_bounds["max"],
                    ),
                ),
                dash='solid',
                color=color,
                width=2,
            ),
        )

        merge(
            structure,
            content,
        )

    def get_data(self):
        return self.get_container()
