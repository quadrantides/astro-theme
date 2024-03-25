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

        structure = dict(
            opacity=1.0,
            visible=True,
            name="positions",
            show_legend=True,
            marker=dict(
                x=[],
                y=[],
                opacity=1.0,
                visible=True,
                hoverinfo='name',
                symbol="square",
                size=3,
                color="#888",
                line=dict(
                    color="",
                    width=1.0,
                ),
                # hovertemplate="" +
                #               "<i>%{customdata[2]}</i><br>" +
                #               "<i> %{customdata[3]}</i><br>" +
                #               "<i> %{customdata[1]}</i><br>" +
                #               "<i>%{customdata[4]}</i>",
                hovertemplate="" +
                              "<i>%{customdata[0]}</i><br>" +
                              "<i> %{customdata[1]}</i><br>" +
                              "<i> %{customdata[2]}</i><br>"
            ),
        )

        merge(
            structure,
            content,
        )

    def get_data(self):
        return self.get_container()
