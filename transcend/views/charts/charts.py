# coding=utf-8
"""
Created on 2020, April 26th
@author: orion
"""
import copy


class Chart(object):

    def __init__(self, theme, name, content, sub_name=''):

        # properties
        self.theme = ""
        self.name = ""
        self.sub_name = ""
        self.content = dict()

        # initialization
        self.theme = theme
        self.name = name
        self.content = content
        self.sub_name = sub_name

    def get_theme(self):
        return self.theme

    def get_name(self):
        return self.name

    def get_content(self):
        return self.content

    def get_sub_name(self):
        return self.sub_name

    def has_sub_name(self):
        return self.get_sub_name()

    def get_structure(self):
        # chart name
        structure = dict(
            chart={self.get_name(): dict()}
        )
        content = copy.deepcopy(
            self.get_content(),
        )
        # sub chart name
        if self.has_sub_name():
            structure[self.get_name()].update(
                {self.get_sub_name(): content}
            )
        else:
            structure[self.get_name()] = content

        return structure
