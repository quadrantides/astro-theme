# coding=utf-8
"""
Created on 2020, April 11th
@author: orion
"""
from transcend.containers import Container


class Model(Container):

    def __init__(self, chart_name, sub_chart_name=""):
        super(Model, self).__init__(container=chart_name)
        self.chart_name = "theme"
        self.sub_chart_name = sub_chart_name

    def get_sub_chart_name(self):
        return self.get_container().get_sub_name()

    def get_chart_name(self):
        return self.get_container().get_name()

    def get_theme(self):
        return self.get_container().get_theme()

    def load(self):
        pass
