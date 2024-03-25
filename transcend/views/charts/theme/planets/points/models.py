# coding=utf-8
"""
Created on 2020, April 28th
@author: orion
"""
from transcend.processes import merge

from transcend.views.charts.graphics.models import Model as GraphicsModel
from transcend.views.charts.theme.models import Model as BaseModel


class Model(BaseModel, GraphicsModel):

    def __init__(self, chart, dimensions=None):
        BaseModel.__init__(self, chart)
        GraphicsModel.__init__(self, dimensions=dimensions)
        self.init()

    def init(self):
        self.load_chart()

    def load_chart(self):
        chart = self.get_container()

        points_bounds = self.get_points_lines()['radius']

        external_radius = self.get_houses_lines()['radius']['max']
        annotation_radius = external_radius

        content = chart.get_content()

        color = self.dimensions["points"]['line']['color']

        structure = dict(
            opacity=0.65,
            visible=True,
            name="point of interest [ASC or MC",
            annotation=dict(
                radius=annotation_radius,
                xanchor="center",
                yanchor="top",
                font=dict(
                    color="#ffffff",
                    size=15,
                ),
                arrowcolor="#bf7704",
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
