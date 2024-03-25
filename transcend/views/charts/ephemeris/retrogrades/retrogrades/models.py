# coding=utf-8
"""
Created on 2020, December 6th
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
            name="retrogrades",
            annotation=dict(
                opacity=0.75,
                xanchor="center",
                yanchor="middle",
                textposition="center middle",
                font=dict(
                    family='sans-serif',
                    color="#000",
                    size=12,
                ),
                layer="above",
            ),
            marker=dict(
                radius=dict(
                    min=graduations["radius"]["max"],
                    max=0.95,
                ),
                opacity=0.25,
                visible=True,
                symbol="circle",
                size=1,
                color="#888",
                line=dict(
                    color="#888",
                    width=0.5,
                ),
            ),
            line=dict(
                hover_template="%{customdata[0]}",
                # hover_template="%{customdata[0]}<br><br>" +
                #                " period : %{customdata[1]} days<br><br>" +
                #                " %{customdata[2]}<br>" +
                #                " %{customdata[3]} %{customdata[4]}<br><br>" +
                #                " %{customdata[5]}<br>" +
                #                " %{customdata[6]} %{customdata[7]}<br>",
                points=dict(
                    begin=dict(
                        radius=0.0,
                        angle=0.0,
                    ),
                    end=dict(
                        radius=0.0,
                        angle=0.0,
                    ),
                ),
                dash='solid',
                color="#000",
                width=8,
            ),
        )

        merge(
            structure,
            content,
        )

    def get_data(self):
        return self.get_container()
