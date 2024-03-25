# coding=utf-8
"""
Created on 2020, December 14th
@author: orion
"""
import datetime
import numpy as np
import plotly.express as px
from plotly import graph_objects as go

from astro.planets.positions.ephemeris.views.constants import DIMENSIONS

from transcend.views.charts.theme.graphics.graphics import Graphic as BaseGraphic

# from transcend.views.charts.theme.tropical.subtitles.constants import get_structure as get_subtitles_structure
# from transcend.views.charts.theme.tropical.subtitles.processes import Process as SubtitlesProcess

# ZODIACS

from astro.legend.zodiac.charts import get_process_chart as get_zodiac_process_chart
from astro.legend.zodiac.charts import get_view_chart as get_zodiac_view_chart

from astro.legend.zodiac.models import Model as ZodiacModel
from astro.legend.zodiac.processes import Process as ZodiacProcess


# POSITIONS

from astro.models.positions.processes import Process as PositionsModelProcess

from astro.planets.positions.ephemeris.views.processes import Process as PositionsProcess
from astro.planets.positions.ephemeris.views.charts import get_process_chart as get_positions_process_chart
from astro.planets.positions.ephemeris.views.charts import get_view_chart as get_positions_view_chart
from astro.planets.positions.ephemeris.views.models import Model as PositionsModel

DATE_FORMAT = "%Y%m%d"


df = px.data.gapminder()
print("ok")

def get_config():
    return {'displayModeBar': False}


class Graphic(BaseGraphic):

    def __init__(self, model, title, view_type):
        super(Graphic, self).__init__(model, title)
        self.type = ""

        zodiactype = ""

        zodiactype = "tropical"
        self.type = view_type
        self.add_legend(zodiactype)

        self.add_positions()

        self.create()

    def get_view_type(self):
        return self.type

    def add_legend(self, zodiactype):

        zodiac_model = ZodiacModel(
            get_zodiac_view_chart(
                zodiactype,
            ),
        )

        process = ZodiacProcess(
            self.get_container().get_data()["zodiac"],
            get_zodiac_process_chart(
            ),
            zodiac_model,
        )

        self.add(
            process.get_graphics_components()
        )

    def add_zodiac_legend(self, data_model, view_model):
        pass

    # def get_xrange(self):
    #     pass

    def add_positions(
            self,
            graphics_dimensions=None,
    ):
        pass
        # process_model = PositionsModelProcess(
        #     self.get_container().get_data(),
        # )
        # view_model = PositionsModel(
        #     get_positions_view_chart(),
        # )
        # process = PositionsProcess(
        #     process_model,
        #     get_positions_process_chart(),
        #     view_model=view_model,
        #     graphics_dimensions=graphics_dimensions,
        # )
        #
        # self.add(
        #     process.get_graphics_components()
        # )

    # def add_subtitles(self, identifier):
    #     process = SubtitlesProcess(
    #         self.get_container().get_tropical(),
    #         get_subtitles_structure(),
    #         identifier,
    #     )
    #     self.add(
    #         process.get_graphics_components()
    #     )

    def create(self):

        self.set_graphic(
            go.Figure(
                **self.get_graphic_data(),
            )
        )

        self.graphic.update_xaxes(
            range=self.get_xrange(),
        )

        # self.graphic.data[10].update(xaxis='x2')

        start = self.get_container().get_request()["date"]["start"]
        end = self.get_container().get_request()["date"]["end"]

        # self.graphic.update_xaxes(
        #
        #     xaxis_tickformatstops=[
        #         dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
        #         dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
        #         dict(dtickrange=[60000, 3600000], value="%H:%M m"),
        #         dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
        #         dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
        #         dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
        #         dict(dtickrange=["M1", "M12"], value="%b '%y M"),
        #         dict(dtickrange=["M12", None], value="%Y Y")
        #     ]
        # )

        # self.graphic.update_xaxes(
        #     ticks="outside",
        #     tickwidth=1,
        #     tickcolor='#000',
        #     ticklen=DIMENSIONS['layout']['xaxis']['ticklen'],
        #     tickformatstops=[
        #         dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
        #         dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
        #         dict(dtickrange=[60000, 3600000], value="%H:%M m"),
        #         dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
        #         dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
        #         dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
        #         dict(dtickrange=["M1", "M12"], value="%d %m '%Y"),
        #         dict(dtickrange=["M12", None], value="%Y Y")
        #     ]
        # )

        request = self.get_container().get_request()

        start_date = request["date"]["start"]
        end_date = request["date"]["end"]

        output_type = self.get_container().get_output_type()
        if output_type == "html":
            self.graphic.write_html(
                "{}_view_planets_longitudes_{}_{}.html".format(
                    self.get_view_type(),
                    start_date.strftime(DATE_FORMAT),
                    end_date.strftime(DATE_FORMAT),
                ),
                config=get_config(),
            )
        elif output_type == "json":
            self.graphic.write_json(
                "{}_view_planets_longitudes_{}_{}.json".format(
                    self.get_view_type(),
                    start_date.strftime(DATE_FORMAT),
                    end_date.strftime(DATE_FORMAT),
                ),
            )
        # config = get_config()
        # print(config)

    # def add_zodiac_legend(self, data_model, view_model):
    #
    #     data_model["graphic"] = dict()
    #     data_model["graphic"]["xaxis"] = dict()
    #     data_model["graphic"]["xaxis"]["range"] = self.get_xrange()
    #
    #     data_model["graphic"]["text"] = dict()
    #     data_model["graphic"]["text"]["x0"] = \
    #         data_model["graphic"]["xaxis"]["range"][0] + datetime.timedelta(days=10)
    #
    #     process = ZodiacProcess(
    #         data_model,
    #         get_zodiac_process_chart(
    #         ),
    #         view_model,
    #     )
    #
    #     self.add(
    #         process.get_graphics_components()
    #     )

    def get_xrange(self):
        start = self.get_container().get_request()["date"]["start"]
        end = self.get_container().get_request()["date"]["end"]

        return [start - datetime.timedelta(days=25), end]

    def prevent_empty_graph_bug(self):
        if len(self.get_traces()) == 0:
            # plotly ne sait pas afficher un graphe vide avec un xrange datetime
            self.add_traces(
                [go.Scatter(x=[self.get_xrange()[0]], y=[0], showlegend=False, marker=dict(color=["#fff"]))]
            )

    def get_graphic_data(self):

        self.prevent_empty_graph_bug()

        annotations = self.get_annotations()
        images = self.get_images()
        traces = self.get_traces()
        shapes = self.get_shapes()

        l = r = b = t = 100
        layout = go.Layout(
            template="plotly_white",
            dragmode=False,
            hovermode='closest',
            title="Astronomical Point of View",
            margin=dict(
                l=l,
                r=r,
                b=b,
                t=t,
                pad=0,
            ),
            font=dict(
                family='sans-serif',
                size=8,
                color='#000',
            ),
            legend=dict(
                x=0.0,
                y=1.1,
                title="",
                orientation="h",
                traceorder='normal',
                itemsizing="constant",
                font=dict(
                    family='sans-serif',
                    size=8,
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
                # fixedrange=True,
                visible=True,
                range=self.get_xrange(),
                dtick="M1",
                tickformat="%b\n%Y",
                ticks="outside",
                tickwidth=1,
                tickcolor='#000',
                ticklen=DIMENSIONS['layout']['xaxis']['ticklen'],
            ),
            yaxis=dict(
                # fixedrange=True,
                visible=True,
                range=DIMENSIONS['layout']['yaxis']['range'],
                tickvals=np.array(range(12)) * 30,
                ticks="outside",
                tickwidth=1,
                tickcolor='#000',
                ticklen=DIMENSIONS['layout']['xaxis']['ticklen'],
            ),
            annotations=annotations,
            images=images,
            shapes=shapes,

        )

        return dict(
            data=traces,
            layout=layout,
        )
