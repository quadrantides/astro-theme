# coding=utf-8
"""
Created on 2020, December 6th
@author: orion
"""
from transcend.containers import Container

from transcend.models.retrogrades.retrograde.processes import Process as RetrogradesProcess


class Process(Container):

    def __init__(self, data):
        super(Process, self).__init__(data)

        # real planets model description

        self.retrogrades = RetrogradesProcess(
            self.get_container(),
        )
        self.set_retrogrades()
        self.data = dict()

    def set_retrogrades(self):
        self.retrogrades.process()

    def get_retrogrades(self):
        return self.retrogrades.get_data()

    def get_zodiac(self):
        return self.get_container()['zodiac']

    def get_data(self):
        return {
            'chart': {
                'retrogrades': self.retrogrades.get_data(),
            },
        }
