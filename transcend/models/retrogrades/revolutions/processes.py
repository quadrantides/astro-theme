# coding=utf-8
"""
Created on 2020, December 8th
@author: orion
"""
from transcend.models.retrogrades.retrograde.processes import Process as RetrogradesProcess


class Process(RetrogradesProcess):

    def __init__(self, data):
        super(Process, self).__init__(data)

    def get_data(self):
        revolutions = None
        retrogrades = self.get_data()
        return {
            'chart': {
                'revolutions': revolutions,
            },
        }
