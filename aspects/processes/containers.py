# -*- coding: utf-8 -*-
"""
Created on 2020, April 11th
@author: orion

"""


class Container(object):

    def __init__(self, container=None):
        self.container = None
        self.set_container(container)

    def get_container(self):
        return self.container

    def set_container(self, container):
        self.container = container
