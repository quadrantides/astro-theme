# coding=utf-8
"""
Created on 2020, May 7th
@author: orion
"""
from transcend.views.charts.theme.planets.aspects.processes import Process as BaseProcess

# GRADUATIONS

from transcend.views.charts.theme.graduations.processes import Process as GraduationsProcess
from transcend.views.charts.theme.compounded.planets.aspects.graduations.models import Model as GraduationsModel


class Process(BaseProcess):

    def __init__(self, data_model, process_model, view_model=None, load_only=True):
        super(Process, self).__init__(
            data_model,
            process_model,
            view_model=view_model,
            load_only=load_only,
        )

    def load_graduations(self):
        self.processes['graduations'] = self.get_aspects_graduations(
            GraduationsProcess,
            GraduationsModel,
        )
