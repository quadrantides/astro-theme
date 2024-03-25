# coding=utf-8
"""
Created on 2020, May 7th
@author: orion
"""
from transcend.processes import merge
from transcend.views.charts.theme.compounded.geometries.models import Model as BaseModel

GRAPHICS_DEFAULT_NAME = 'aspect'


class Model(BaseModel):

    def __init__(self, chart, sub_chart_name=""):
        super(Model, self).__init__(chart, sub_chart_name=sub_chart_name)
        self.init()

    def init(self):
        self.load()

    def load(self):
        chart = self.get_container()

        aspects_radius = self.get_aspects_circle_radius(zodiactype="sidereal")
        # conjunction_radius = self.get_conjunction_radius()

        content = chart.get_content()

        structure = dict(
            opacity=0.75,
            visible=True,
            name=GRAPHICS_DEFAULT_NAME,
            circle=dict(
                radius=aspects_radius,
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
                size=1.25,
                hovertemplate="" +
                              "%{customdata[0]}",
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
