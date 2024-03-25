# coding=utf-8
"""
Created on 2020, April 22th
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

        lines_houses_bounds = self.get_houses_lines()

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
                width=1.0,
            ),
            annotation=dict(
                label="",
                x=0.0,
                y=0.0,
                radius=self.get_houses_annotations()["radius"],
                xanchor="center",
                yanchor="middle",
                font=dict(
                    color="#444",
                    size=12,
                ),
            ),
        )

        merge(
            structure,
            content,
        )

    def get_data(self):
        return self.get_container()
