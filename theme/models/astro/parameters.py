# coding=utf-8
"""
Created on 2020, May 12th
@author: orion
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from .tropical.parameters import Parameters as TropicalParameters
from .sidereal.parameters import Parameters as SiderealParameters


class Parameters(models.Model):

    tropical = models.ForeignKey(TropicalParameters, on_delete=models.CASCADE)
    sidereal = models.ForeignKey(SiderealParameters, on_delete=models.CASCADE)

    class Meta:
        app_label = 'theme'
        abstract = True

    def __str__(self):
        return "Parameters, Tropical = {}, Sidereal = {}".format(
            self.tropical,
            self.sidereal,
        )
