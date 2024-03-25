# coding=utf-8
"""
Created on 2020, April 21th
@author: orion
"""
from plotly import graph_objects as go

from transcend.views.charts.graphics.constants import DIMENSIONS
from transcend.views.charts.theme.graphics.graphics import Graphic as BaseGraphic

from transcend.views.charts.theme.sidereal.subtitles.constants import get_structure as get_subtitles_structure
from transcend.views.charts.theme.sidereal.subtitles.processes import Process as SubtitlesProcess

# HOUSES

from transcend.views.charts.theme.houses.models import Model as HousesModel

# ZODIAC

from transcend.views.charts.theme.zodiac.models import Model as ZodiacModel


class Graphic(BaseGraphic):

    def __init__(self, model, title):
        super(Graphic, self).__init__(model, title)

        self.add_subtitles()

        # self.add_graduations("theme", "sidereal")

        self.add_houses(
            "theme",
            "tropical",
            self.get_container().get_sidereal(),
            HousesModel,
        )

        self.add_zodiac(
            "theme",
            "sidereal",
            self.get_container().get_sidereal(),
            ZodiacModel,
        )

        self.add_planets(
            self.get_container(),
            "theme",
            "sidereal",
        )

        self.create()

    def add_subtitles(self):
        process = SubtitlesProcess(
            self.get_container().get_sidereal(),
            get_subtitles_structure(),
        )
        self.add(
            process.get_graphics_components()
        )

    def get_graphic_data(self):

        annotations = self.get_annotations()
        images = self.get_images()
        traces = self.get_traces()

        l = r = b = t = 70
        layout =go.Layout(
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
                visible=False,
                fixedrange=True,
                range=DIMENSIONS['layout']['xaxis']['range'],
            ),
            yaxis=dict(
                visible=False,
                fixedrange=True,
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
                    showline=False,
                    linecolor='#444',
                    dtick=2,
                    thetaunit="degrees",
                    gridcolor="#fff",
                    gridwidth=1,
                    showticklabels=False,
                    ticks='inside',
                    ticklen=DIMENSIONS['layout']['polar']['angularaxis']['ticklen'],
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
