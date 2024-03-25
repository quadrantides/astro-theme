# coding=utf-8
"""
Created on 2020, April 30th
@author: orion
"""
from transcend.processes import merge
from transcend.views.charts.graphics.models import Model as GraphicsModel
from transcend.views.charts.theme.models import Model as BaseModel


GRAPHICS_DEFAULT_NAME = 'aspect'


class Model(BaseModel, GraphicsModel):

    def __init__(self, chart, dimensions=None):
        BaseModel.__init__(self, chart)
        GraphicsModel.__init__(self, dimensions=dimensions)
        self.init()

    def init(self):
        self.load_chart()

    def load_chart(self):
        chart = self.get_container()

        aspects_radius_in_polar_coords = self.get_aspects_radius()
        # conjunction_radius = self.get_conjunction_radius()
        content = chart.get_content()

        structure = dict(
            opacity=0.75,
            visible=True,
            name=GRAPHICS_DEFAULT_NAME,
            circle=dict(
                radius=aspects_radius_in_polar_coords,
                line=dict(
                    dash='solid',
                    color="#444",
                    width=1,
                ),
            ),
            marker=dict(
                opacity=1.0,
                visible=True,
                symbol="square",
                size=8,
                hovertemplate="" +
                              "%{customdata[0]}",
            ),
            line=dict(
                opacity=1.0,
                visible=True,
                hovertemplate='%{name}',
                points=dict(
                    planet1=dict(
                        radius=aspects_radius_in_polar_coords,
                    ),
                    planet2=dict(
                        radius=aspects_radius_in_polar_coords,
                    ),
                ),
                line=dict(
                    dash='solid',
                    width=1,
                ),
            ),
            # conjunction=dict(
            #     radius=conjunction_radius,
            # )
        )

        merge(
            structure,
            content,
        )

    def get_data(self):
        return self.get_container()
