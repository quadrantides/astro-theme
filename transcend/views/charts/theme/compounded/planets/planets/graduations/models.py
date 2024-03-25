# coding=utf-8
"""
Created on 2020, May 7th
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

        dtick = DIMENSIONS["layout"]['polar']['angularaxis']['dtick']
        graduations = self.get_planets_graduations()

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
                        # thicklen=0.0,
                    ),
                    others=dict(
                        color="#444",
                        width=1.0,
                        # thicklen=0.0,
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
