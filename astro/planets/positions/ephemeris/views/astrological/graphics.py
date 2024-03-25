# coding=utf-8
"""
Created on 2020, December 19th
@author: orion
"""
import numpy as np
import datetime
from plotly import graph_objects as go

from astro.planets.positions.ephemeris.views.constants import DIMENSIONS

from astro.planets.positions.ephemeris.views.graphics import Graphic as Base

# POSITIONS

from astro.models.positions.processes import Process as PositionsModelProcess

from astro.planets.positions.ephemeris.views.astrological.processes import Process as PositionsProcess
from astro.planets.positions.ephemeris.views.astrological.charts import get_process_chart as get_positions_process_chart
from astro.planets.positions.ephemeris.views.astrological.charts import get_view_chart as get_positions_view_chart
from astro.planets.positions.ephemeris.views.astrological.models import Model as PositionsModel

# ZODIACS

from astro.legend.zodiac.astrological.charts import get_process_chart as get_zodiac_process_chart
from astro.legend.zodiac.astrological.charts import get_view_chart as get_zodiac_view_chart

from astro.legend.zodiac.astrological.models import Model as ZodiacModel
from astro.legend.zodiac.astrological.processes import Process as ZodiacProcess


class Graphic(Base):

    def __init__(self, model, title):
        super(Graphic, self).__init__(model, title, "astrological")

    def add_legend(self, zodiactype):

        zodiac_model = ZodiacModel(
            get_zodiac_view_chart(
                zodiactype,
            ),
        )
        data_model = self.get_container().get_data()
        data_model["graphic"] = dict()
        data_model["graphic"]["xaxis"] = dict()
        data_model["graphic"]["xaxis"]["range"] = self.get_xrange()
        # data_model["graphic"]["zodiac_shape_xrange"] = self.get_zodiac_shape_xrange()
        data_model["graphic"]["background_shape_xrange"] = self.get_background_shape_xrange()

        process = ZodiacProcess(
            data_model,
            get_zodiac_process_chart(
            ),
            zodiac_model,
        )

        self.add(
            process.get_graphics_components()
        )

    def add_positions(
            self,
            graphics_dimensions=None,
    ):

        process_model = PositionsModelProcess(
            self.get_container().get_data(),
        )
        view_model = PositionsModel(
            get_positions_view_chart(),
        )
        process = PositionsProcess(
            process_model,
            get_positions_process_chart(),
            view_model=view_model,
            graphics_dimensions=graphics_dimensions,
        )

        self.add(
            process.get_graphics_components()
        )

    def get_zodiac_shape_xrange(self):
        start = self.get_xrange()[0]
        return [start, start + datetime.timedelta(days=4)]

    def get_background_shape_xrange(self):
        return [self.get_zodiac_shape_xrange()[1], self.get_xrange()[1]]

    def get_xrange(self):
        start = self.get_container().get_request()["date"]["start"]
        end = self.get_container().get_request()["date"]["end"]

        return [start - datetime.timedelta(days=2), end]

    def get_graphic_data(self):

        self.prevent_empty_graph_bug()

        annotations = self.get_annotations()
        images = self.get_images()
        traces = self.get_traces()
        shapes = self.get_shapes()

        l = r = 50
        t = 80
        b = 50

        layout = go.Layout(
            template="plotly_white",
            dragmode=False,
            hovermode='closest',
            # title="Astrological Point of View",
            margin=dict(
                l=l,
                r=r,
                b=b,
                t=t,
                pad=0,
            ),
            font=dict(
                family='sans-serif',
                size=10,
                color='#000',
            ),
            legend=dict(
                x=0.0,
                y=1.15,
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
                ticks="outside",
                tickwidth=1,
                tickcolor='#000',
                showspikes=True, spikedash='solid', spikemode='across',
                spikecolor="grey", spikesnap="cursor", spikethickness=2,
                ticklen=DIMENSIONS['layout']['xaxis']['ticklen'],
                tickformatstops=[
                    dict(dtickrange=[None, 60000], value="%e. %b %H h"),
                    dict(dtickrange=[60000, 3600000], value="%e. %b %H h"),
                    dict(dtickrange=[3600000, 86400000], value="%e. %b %H h"),
                    dict(dtickrange=[86400000, 604800000], value="%e. %b"),
                    dict(dtickrange=[604800000, "M1"], value="%e. %b"),
                    dict(dtickrange=["M1", "M12"], value="%b %Y"),
                    dict(dtickrange=["M12", None], value="%Y")
                ],
            ),
            xaxis2=dict(
                title="Date",
                overlaying="x",
                side="top",
            ),
            yaxis=dict(
                fixedrange=True,
                visible=True,
                dtick=30,
                range=DIMENSIONS['layout']['yaxis']['range'],
                tickvals=np.array(range(12)) * 30,
                ticks="outside",
                tickwidth=1,
                tickcolor='#000',
                ticklen=DIMENSIONS['layout']['yaxis']['ticklen'],
                ticktext=[""] * 12,
                # showspikes=True, spikedash='solid', spikemode='across',
                # spikecolor="grey", spikesnap="cursor", spikethickness=1,
            ),
            annotations=annotations,
            images=images,
            shapes=shapes,


        )

        return dict(
            data=traces,
            layout=layout,
        )
