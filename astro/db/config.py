# -*- coding: utf-8 -*-
"""
Created on 2019 November, 6th
@author: pjournoud
"""
from configparser import ConfigParser

from astro.db.exceptions import ConfigSectionNotFound


class Config(object):
    def __init__(self, filename='quadrantides.ini', section='default', init=True):
        self.filename = filename
        self.section = section
        self.data = dict()
        if init:
            self.init()

    def init(self):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(self.filename)

        # get section

        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                self.data[param[0]] = param[1]
        else:
            raise ConfigSectionNotFound(self.section, self.filename)

    def get(self):
        return self.data
