# coding=utf-8
"""
Created on 2020, June 9th
@author: orion
"""


class Process(object):

    def __init__(self, logger=None):
        super(Process, self).__init__()
        self.logger = logger

    def add_logger(self, logger):
        self.logger = logger

    def get_logger(self):
        return self.logger
