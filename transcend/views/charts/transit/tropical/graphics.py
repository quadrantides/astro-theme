# coding=utf-8
"""
Created on 2020, August 13th
@author: orion
"""
from plotly import graph_objects as go

from transcend.views.charts.theme.graphics.graphics import Graphic as BaseGraphic

from transcend.views.charts.theme.tropical.subtitles.constants import get_structure as get_subtitles_structure
from transcend.views.charts.transit.tropical.subtitles.processes import Process as SubtitlesProcess

# HOUSES

from transcend.views.charts.theme.houses.models import Model as HousesModel
from transcend.views.charts.theme.houses.charts import get_view_chart as get_houses_view_chart
from transcend.views.charts.transit.graphics.theme.constants import DIMENSIONS as theme_graphic_dimensions
from transcend.views.charts.transit.graphics.transit.constants import DIMENSIONS as transit_graphic_dimensions

# ZODIAC

from transcend.views.charts.theme.zodiac.models import Model as ThemeZodiacModel
from transcend.views.charts.theme.zodiac.charts import get_view_chart as get_zodiac_view_chart

# PLANETS

from transcend.models.planets.processes import Process as PlanetsModelProcess

from transcend.views.charts.theme.planets.processes import Process as PlanetsProcess
from transcend.views.charts.theme.planets.charts import get_process_chart as get_planets_process_chart


class Graphic(BaseGraphic):

    def __init__(self, model, title):
        super(Graphic, self).__init__(model, title)
        zodiactype = "tropical"
        self.add_subtitles(
            theme_identifier=model.get_theme_identifier(zodiactype),
            transit_identifier=model.get_transit_identifier(zodiactype),
        )

        # THEME part of the graphic

        houses_model = HousesModel(
            get_houses_view_chart("theme", "tropical"),
            dimensions=theme_graphic_dimensions,
        )

        self.add_houses(
            "theme",
            "tropical",
            self.get_container().get_tropical()['houses'],
            houses_model,
        )

        zodiac_model = ThemeZodiacModel(
            get_zodiac_view_chart(
                "theme",
                "tropical",
                customize_values=True,
            ),
            dimensions=theme_graphic_dimensions,
        )
        self.add_zodiac(
            "theme",
            "tropical",
            self.get_container().get_tropical()['zodiac'],
            zodiac_model,
            customize_values=True,
        )

        self.add_planets(
            self.get_container(),
            "theme",
            "tropical",
            show_aspects=False,
            # show_points=False,
            graphics_dimensions=theme_graphic_dimensions,
        )

        # TRANSIT part of the graphic

        # houses_model = HousesModel(
        #     get_houses_view_chart("transit", "tropical"),
        #     dimensions=transit_graphic_dimensions,
        # )
        #
        # self.add_houses(
        #     "transit",
        #     "tropical",
        #     self.get_container().get_tropical()['transit']['houses'],
        #     houses_model,
        # )

        process_model = PlanetsModelProcess(
            self.get_container(),
        )
        process = PlanetsProcess(
            get_planets_process_chart(
                "transit",
                "tropical",
                process_model,
            ),
            show_aspects=True,
            show_points=False,
            show_annotations=False,
            graphics_dimensions=transit_graphic_dimensions,
        )

        self.add(
            process.get_graphics_components()
        )
        self.create()

    def add_subtitles(self, theme_identifier, transit_identifier):
        process = SubtitlesProcess(
            self.get_container().get_tropical(),
            get_subtitles_structure(),
            theme_identifier,
            transit_identifier,
        )
        self.add(
            process.get_graphics_components()
        )

    def get_graphic_data(self):
        annotations = self.get_annotations()
        images = self.get_images()
        traces = self.get_traces()

        l = r = b = t = 70
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
            width=transit_graphic_dimensions['layout']['width'],
            height=transit_graphic_dimensions['layout']['height'],
            xaxis=dict(
                fixedrange=True,
                visible=False,
                range=transit_graphic_dimensions['layout']['xaxis']['range'],
            ),
            yaxis=dict(
                fixedrange=True,
                visible=False,
                range=transit_graphic_dimensions['layout']['yaxis']['range'],
            ),
            polar=dict(
                domain=dict(
                    x=transit_graphic_dimensions['layout']['polar']['domain']['x'],
                    y=transit_graphic_dimensions['layout']['polar']['domain']['y'],
                ),
                bgcolor="rgb(255, 2555, 255)",
                angularaxis=dict(
                    visible=False,
                    linewidth=1,
                    showline=True,
                    linecolor='#444',
                    dtick=10,
                    thetaunit="degrees",
                    gridcolor="#fff",
                    gridwidth=1,
                    showticklabels=False,
                    ticks='outside',
                    ticklen=transit_graphic_dimensions['layout']['polar']['angularaxis']['ticklen'],
                ),
                radialaxis=dict(
                    visible=False,
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
