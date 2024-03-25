# coding=utf-8
"""
Created on 2020, December 6th
@author: orion
"""
from plotly import graph_objects as go

from transcend.views.charts.ephemeris.retrogrades.constants import DIMENSIONS
from transcend.views.charts.theme.graphics.graphics import Graphic as BaseGraphic

# from transcend.views.charts.theme.tropical.subtitles.constants import get_structure as get_subtitles_structure
# from transcend.views.charts.theme.tropical.subtitles.processes import Process as SubtitlesProcess

# ZODIAC

from transcend.views.charts.theme.zodiac.models import Model as ZodiacModel
from transcend.views.charts.theme.zodiac.charts import get_view_chart as get_zodiac_view_chart

# RETROGRADES

from transcend.models.retrogrades.processes import Process as RetrogradesModelProcess

from transcend.views.charts.ephemeris.retrogrades.processes import Process as RetrogradesProcess
from transcend.views.charts.ephemeris.retrogrades.charts import get_process_chart as get_retrogrades_process_chart


class Graphic(BaseGraphic):

    def __init__(self, model, title):
        super(Graphic, self).__init__(model, title)

        zodiactype = "default"

        zodiac_model = ZodiacModel(
            get_zodiac_view_chart(
                "theme",
                zodiactype,
                customize_values=True,
            ),
        )
        self.add_zodiac(
            "theme",
            zodiactype,
            self.get_container()["zodiac"],
            zodiac_model,
            customize_values=True,
        )

        self.add_retrogrades()

        self.create()

    def add_retrogrades(
            self,
            graphics_dimensions=None,
    ):
        theme = ""
        chart_name = "retrogrades"

        process_model = RetrogradesModelProcess(
            self.get_container()["retrogrades"],
        )
        process = RetrogradesProcess(
            get_retrogrades_process_chart(
                theme,
                chart_name,
                process_model,
            ),
            graphics_dimensions=graphics_dimensions,
        )

        self.add(
            process.get_graphics_components()
        )

    # def add_subtitles(self, identifier):
    #     process = SubtitlesProcess(
    #         self.get_container().get_tropical(),
    #         get_subtitles_structure(),
    #         identifier,
    #     )
    #     self.add(
    #         process.get_graphics_components()
    #     )

    def get_graphic_data(self):
        annotations = self.get_annotations()
        images = self.get_images()
        traces = self.get_traces()
        print("ok")

        l = r = b = t = 10
        layout = go.Layout(
            template="plotly_white",
            dragmode=False,
            hovermode='closest',
            title=None,
            margin=dict(
                l=l,
                r=r,
                b=b,
                t=t,
                pad=0,
            ),
            legend=dict(
                x=0.05,
                y=-0.05,
                title="",
                orientation="h",
                traceorder='normal',
                itemsizing="constant",
                font=dict(
                    family='sans-serif',
                    size=10,
                    color='#000',
                ),
                bgcolor='#fff',
                bordercolor='#fff',
                borderwidth=1,
            ),
            showlegend=True,
            width=DIMENSIONS['layout']['width'],
            height=DIMENSIONS['layout']['height'],
            xaxis=dict(
                fixedrange=True,
                visible=False,
                range=DIMENSIONS['layout']['xaxis']['range'],
            ),
            yaxis=dict(
                fixedrange=True,
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
                    visible=True,
                    linewidth=1,
                    showline=True,
                    linecolor='#444',
                    dtick=30,
                    thetaunit="degrees",
                    gridcolor="#444",
                    gridwidth=1,
                    showticklabels=False,
                    ticks='outside',
                    ticklen=DIMENSIONS['layout']['polar']['angularaxis']['ticklen'],
                ),
                radialaxis=dict(
                    visible=False,
                    tickmode="array",
                    # tickvals=2 * categoryarray,
                    showticklabels=False,
                    side="counterclockwise",
                    angle=0,
                    showline=False,
                    linewidth=1,
                    tickwidth=0,
                    gridcolor="#fff",
                    range=[0, 1],
                    gridwidth=1
                ),
            ),
            annotations=annotations,
            images=images,

        )
        return dict(
            data=traces,
            layout=layout,
        )

    def create(self):

        self.set_graphic(
            go.Figure(
                **self.get_graphic_data()
            )
        )
