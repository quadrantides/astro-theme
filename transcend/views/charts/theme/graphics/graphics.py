# coding=utf-8
"""
Created on 2020, April 21th
@author: orion
"""
from plotly import graph_objects as go

from transcend.views.charts.graphics.constants import DIMENSIONS
from transcend.views.graphics.graphics import Graphic as BaseGraphic

# ZODIACS

from transcend.views.charts.theme.zodiac.charts import get_process_chart as get_zodiac_process_chart
from transcend.views.charts.theme.zodiac.charts import get_view_chart as get_zodiac_view_chart

# THEME

from transcend.views.charts.theme.zodiac.processes import Process as ZodiacProcess

# HOUSES

from transcend.views.charts.theme.houses.charts import get_process_chart as get_houses_process_chart
from transcend.views.charts.theme.houses.charts import get_view_chart as get_houses_view_chart
from transcend.views.charts.theme.houses.processes import Process as HousesProcess

# PLANETS

from transcend.models.planets.processes import Process as PlanetsModelProcess

from transcend.views.charts.theme.planets.processes import Process as PlanetsProcess
from transcend.views.charts.theme.planets.charts import get_process_chart as get_planets_process_chart


class Graphic(BaseGraphic):

    def __init__(self, model, title):
        super(Graphic, self).__init__(model, title)

    def add_houses(self, theme, chart_name, data_model, view_model, sub_chart_name=""):
        process = HousesProcess(
            data_model,
            get_houses_process_chart(theme, chart_name, sub_chart_name=sub_chart_name),
            view_model,
        )
        self.add(
            process.get_graphics_components()
        )

    def add_zodiac(self, theme, chart_name, data_model, view_model, sub_chart_name="", customize_values=False):

        process = ZodiacProcess(
            data_model,
            get_zodiac_process_chart(
                theme,
                chart_name,
                sub_chart_name=sub_chart_name,
                customize_values=customize_values,
            ),
            view_model,
        )

        self.add(
            process.get_graphics_components()
        )

    def add_planets(
            self,
            data_model,
            theme,
            chart_name,
            sub_chart_name="",
            show_aspects=True,
            show_points=True,
            graphics_dimensions=None,
    ):

        process_model = PlanetsModelProcess(
            data_model,
        )
        process = PlanetsProcess(
            get_planets_process_chart(
                theme,
                chart_name,
                process_model,
                sub_chart_name=sub_chart_name,
            ),
            show_aspects=show_aspects,
            show_points=show_points,
            graphics_dimensions=graphics_dimensions,
        )

        self.add(
            process.get_graphics_components()
        )

    def create(self):

        annotations = self.get_annotations()
        images = self.get_images()
        traces = self.get_traces()
        shapes = self.get_shapes()

        l = r = b = t = 70
        layout =go.Layout(
            template="plotly_white",
            title=self.get_title(),
            margin=dict(
                l=l,
                r=r,
                b=b,
                t=t,
                pad=0,
            ),
            showlegend=True,
            width=DIMENSIONS['layout']['width'],
            height=DIMENSIONS['layout']['height'],
            xaxis=dict(
                visible=False,
                range=DIMENSIONS['layout']['xaxis']['range'],
            ),
            yaxis=dict(
                visible=False,
                range=DIMENSIONS['layout']['yaxis']['range'],
            ),
            polar=dict(
                domain=dict(
                    x=DIMENSIONS['layout']['polar']['domain']['x'],
                    y=DIMENSIONS['layout']['polar']['domain']['y'],
                ),
                bgcolor="rgb(255, 2555, 255)",
                angularaxis=dict(
                    linewidth=1,
                    showline=True,
                    linecolor='#444',
                    dtick=10,
                    thetaunit="degrees",
                    gridcolor="#fff",
                    gridwidth=1,
                    showticklabels=False,
                    ticks='inside',
                    ticklen=10,
                ),
                radialaxis=dict(
                    visible=True,
                    showticklabels=False,
                    side="counterclockwise",
                    angle=0,
                    showline=False,
                    linewidth=0,
                    tickwidth=0,
                    gridcolor="#fff",
                    range=[0, 1],
                    gridwidth=1
                ),
            ),
            annotations=annotations,
            images=images,
            shapes=shapes,

        )

        self.graphic = go.Figure(
            data=traces,
            layout=layout,
        )
