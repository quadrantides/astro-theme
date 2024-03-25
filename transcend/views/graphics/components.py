# coding=utf-8
"""
Created on 2020, April 20th
@author: orion
"""
from transcend.containers import Container


class Components(Container):

    def __init__(self, model, components=None):
        super(Components, self).__init__(model)
        self.title = ""
        if components is None:
            components = {}
        self.traces = []
        self.annotations = []
        self.images = []
        self.shapes = []

        self.init(components)

    def init(self, components):
        if components:
            self.add(components)

    def add(self, components):
        key = 'annotations'
        if key in components.keys():
            self.add_annotations(
                components[key]
            )
        key = 'images'
        if key in components.keys():
            self.add_images(
                components[key]
            )
        key = 'traces'
        if key in components.keys():
            self.add_traces(
                components[key]
            )
        key = 'shapes'
        if key in components.keys():
            self.add_shapes(
                components[key]
            )

    def add_shapes(self, components):
        self.shapes.extend(components)

    def add_traces(self, components):
        self.traces.extend(components)

    def add_images(self, components):
        self.images.extend(components)

    def add_annotations(self, components):
        self.annotations.extend(components)

    def get_annotations(self):
        return self.annotations

    def get_images(self):
        return self.images

    def get_traces(self):
        return self.traces

    def get_shapes(self):
        return self.shapes

    def get_graphics_components(self):
        return {
            'traces': self.traces,
            'images': self.images,
            'shapes': self.shapes,
            'annotations': self.annotations,

        }
