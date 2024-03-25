# coding=utf-8
"""
Created on 2020, December 8th
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
        content = chart.get_content()
        graduations = self.get_graduations()

        structure = dict(
            opacity=0.75,
            visible=True,
            name="revolutions",
            spiral=dict(
                radius=dict(
                    min=graduations["radius"]["max"] + 0.05,
                    max=0.85,
                ),
            ),
            line=dict(
                opacity=0.25,
                visible=True,
                hoverinfo='name',
                dash='dot',
                color="#aaa",
                width=1,
            ),
        )

        merge(
            structure,
            content,
        )

    def get_data(self):
        return self.get_container()
