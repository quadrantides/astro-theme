# coding=utf-8
"""
Created on 2020, April 21th
@author: orion
"""
import json as _json
from plotly.utils import PlotlyJSONEncoder
from plotly import graph_objects as go

from transcend.views.graphics.components import Components as GraphicsComponents


class Graphic(GraphicsComponents):

    def __init__(self, model, title='', components=None):
        if components is None:
            components = {}
        GraphicsComponents.__init__(self, model, components)
        self.title = ""
        self.graphic = None
        self.init(title)
        # if self.get_graphics_components():
        #     if len(self.get_graphics_components().keys()) > 0:
        #         self.create()

    def init(self, title):
        self.set_title(title)

    def set_graphic(self, graphic):
        self.graphic = graphic

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def create(self):
        """"
          basic graphic as an illustration
        """
        annotations = self.get_annotations()
        images = self.get_images()

        layout =go.Layout(
            annotations=annotations,
            images=images,
        )

        traces = self.get_traces()
        self.graphic = go.Figure(
            data=traces,
            layout=layout,
        )
            
    def get_graphic(self, json=True):
        if json:
            return _json.dumps(
                self.graphic,
                cls=PlotlyJSONEncoder,
            )
        else:
            return self.graphic
