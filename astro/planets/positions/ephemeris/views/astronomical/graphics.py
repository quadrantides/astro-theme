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

from astro.planets.positions.ephemeris.views.astronomical.processes import Process as PositionsProcess
from astro.planets.positions.ephemeris.views.charts import get_process_chart as get_positions_process_chart
from astro.planets.positions.ephemeris.views.charts import get_view_chart as get_positions_view_chart
from astro.planets.positions.ephemeris.views.astronomical.models import Model as PositionsModel

# ZODIACS

from astro.legend.zodiac.astronomical.charts import get_process_chart as get_zodiac_process_chart
from astro.legend.zodiac.astronomical.charts import get_view_chart as get_zodiac_view_chart

from astro.legend.zodiac.astronomical.models import Model as ZodiacModel
from astro.legend.zodiac.astronomical.processes import Process as ZodiacProcess


class Graphic(Base):

    def __init__(self, model, title):
        super(Graphic, self).__init__(model, title)

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
        data_model["graphic"]["box_size"] = self.get_zodiac_box_size()

        data_model["graphic"]["text"] = dict()
        data_model["graphic"]["text"]["x0"] = self.get_zodiac_xtext()

        process = ZodiacProcess(
            data_model,
            get_zodiac_process_chart(
            ),
            zodiac_model,
        )

        self.add(
            process.get_graphics_components()
        )

    def get_zodiac_xtext(self):
        x0 = self.get_xrange()[0]
        x1 = self.get_zodiac_box_size()[0]

        return x0 + (x1 - x0)/ 2.0

    def get_zodiac_box_size(self):
        start = self.get_container().get_request()["date"]["start"]

        return [start - datetime.timedelta(days=5), start - datetime.timedelta(days=1)]

    def get_xrange(self):
        start = self.get_container().get_request()["date"]["start"]
        end = self.get_container().get_request()["date"]["end"]

        return [start - datetime.timedelta(days=28), end]

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
                size=10,
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
