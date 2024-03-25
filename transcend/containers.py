# -*- coding: utf-8 -*-
"""
Created on 2020, April 11th
@author: orion

"""
from transcend.identifier import Identifier


class Container(Identifier):

    def __init__(self, container=None, identifier=None):
        super(Container, self).__init__(identifier=identifier)
        self.container = None
        self.set_container(container)

    def get_container(self):
        return self.container

    def set_container(self, container):
        self.container = container