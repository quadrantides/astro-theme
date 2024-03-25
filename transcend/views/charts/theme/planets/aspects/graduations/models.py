# coding=utf-8
"""
Created on 2020, May 7th
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
        self.load()

    def load(self):

        dtick = self.dimensions["layout"]['polar']['angularaxis']['dtick']

        graduations = self.get_graduations()

        rmin = graduations["radius"]["min"]
        rmax = graduations["radius"]["max"]

        chart = self.get_container()
        content = chart.get_content()

        structure = dict(
            opacity=0.5,
            visible=True,
            radius=dict(
                min=rmin,
                max=rmax,
            ),
            name="graduations",
            line=dict(
                dash='solid',
                color="#000",
                width=1,
            ),
            ticks=dict(
                dtick=dtick,
                tick=dict(
                    tens=dict(
                        color="#000",
                        width=1.5,
                    ),
                    others=dict(
                        color="#000",
                        width=1.0,
                    ),
                ),
            ),
        )

        merge(
            structure,
            content,
        )

    def get_data(self):
        return self.get_container()
