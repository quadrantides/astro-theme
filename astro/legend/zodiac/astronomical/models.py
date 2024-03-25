# coding=utf-8
"""
Created on 2020, December 19th
@author: orion
"""
from transcend.processes import merge
from transcend.views.charts.graphics.models import Model as GraphicsModel
from transcend.views.charts.theme.models import Model as BaseModel
from astro.legend.zodiac.astronomical.constants import COLORS


class Model(BaseModel, GraphicsModel):

    def __init__(self, chart, dimensions=None):
        BaseModel.__init__(self, chart)
        GraphicsModel.__init__(self, dimensions=dimensions)

        self.init()

    def init(self):
        self.load_chart()

    def load_chart(self):

        chart = self.get_container()
        chart_name = chart.get_name()

        content = chart.get_content()

        structure = dict(
            colors=COLORS,
            opacity=0.25,
            visible=True,
            name=chart_name,
            shape=dict(
                visible=True,
                name=chart_name,
                opacity=0.75,
                layer="below",
                line=dict(
                    color='#ddd',
                    width=1,
                ),
            ),
            marker=dict(
                name="zodiac names",
                opacity=1.0,
                visible=True,
                color="#000",
            ),
        )

        merge(
            structure,
            content,
        )

    def get_data(self):
        return self.get_container()
